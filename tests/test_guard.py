"""Deterministic limits: what may happen, and how often."""

from __future__ import annotations

import pytest

from conduit.core.agent import Agent, Plan, PlanRequest
from conduit.core.guard import (
    DeterministicGuard,
    GuardRule,
    GuardSettings,
    InMemoryGuardStore,
    intent_hash,
)
from conduit.core.tools import (
    SideEffect,
    ToolCall,
    ToolContext,
    ToolSpec,
    ToolStatus,
)
from tests.conftest import NoParams


def spec(name: str, side_effect: SideEffect = SideEffect.READ, **kwargs) -> ToolSpec:
    return ToolSpec(
        name=name, description="A tool.", params=NoParams, side_effect=side_effect, **kwargs
    )


def call(name: str = "demo.echo", **arguments) -> ToolCall:
    return ToolCall(id="c1", name=name, arguments=arguments)


@pytest.fixture
def store() -> InMemoryGuardStore:
    return InMemoryGuardStore()


@pytest.fixture
def guard(store: InMemoryGuardStore) -> DeterministicGuard:
    return DeterministicGuard(settings=GuardSettings(), store=store)


class TestIntentHash:
    def test_argument_order_does_not_change_the_fingerprint(self) -> None:
        """A planner in a loop rarely emits byte-identical JSON."""
        first = intent_hash(ToolCall(id="a", name="t.x", arguments={"a": 1, "b": 2}))
        second = intent_hash(ToolCall(id="b", name="t.x", arguments={"b": 2, "a": 1}))

        assert first == second

    def test_the_call_id_is_not_part_of_it(self) -> None:
        assert intent_hash(ToolCall(id="a", name="t.x")) == intent_hash(
            ToolCall(id="zzz", name="t.x")
        )

    def test_different_arguments_are_different_intents(self) -> None:
        assert intent_hash(call(stage="nuevo")) != intent_hash(call(stage="cerrado"))


class TestOrdering:
    async def test_the_kill_switch_beats_everything(
        self, guard: DeterministicGuard, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        """Pulling it stops things that would otherwise be perfectly fine."""
        store.stop(ctx.tenant_id)

        decision = await guard.review(call(), spec("demo.echo"), ctx)

        assert not decision.allowed
        assert decision.rule == GuardRule.KILL_SWITCH

    async def test_it_is_scoped_to_the_tenant(
        self, guard: DeterministicGuard, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        store.stop("some-other-tenant")

        assert (await guard.review(call(), spec("demo.echo"), ctx)).allowed

    async def test_resume_lifts_it(
        self, guard: DeterministicGuard, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        store.stop(ctx.tenant_id)
        store.resume(ctx.tenant_id)

        assert (await guard.review(call(), spec("demo.echo"), ctx)).allowed


class TestWhitelist:
    async def test_an_empty_whitelist_admits_everything(
        self, guard: DeterministicGuard, ctx: ToolContext
    ) -> None:
        assert (await guard.review(call(), spec("demo.echo"), ctx)).allowed

    async def test_a_non_empty_whitelist_is_exhaustive(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        guard = DeterministicGuard(
            settings=GuardSettings(whitelist=frozenset({"demo.allowed"})), store=store
        )

        assert (await guard.review(call("demo.allowed"), spec("demo.allowed"), ctx)).allowed
        denied = await guard.review(call("demo.other"), spec("demo.other"), ctx)
        assert not denied.allowed
        assert denied.rule == GuardRule.NOT_WHITELISTED


class TestWrites:
    async def test_writes_are_denied_by_default(
        self, guard: DeterministicGuard, ctx: ToolContext
    ) -> None:
        """A deployment that has not said yes cannot mutate anything."""
        decision = await guard.review(call("demo.write"), spec("demo.write", SideEffect.WRITE), ctx)

        assert not decision.allowed
        assert decision.rule == GuardRule.WRITES_DISABLED

    async def test_writes_pass_once_enabled(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        guard = DeterministicGuard(settings=GuardSettings(allow_writes=True), store=store)

        decision = await guard.review(call("demo.write"), spec("demo.write", SideEffect.WRITE), ctx)

        assert decision.allowed

    async def test_a_tool_wanting_confirmation_is_held(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        guard = DeterministicGuard(settings=GuardSettings(allow_writes=True), store=store)
        risky = spec("demo.write", SideEffect.WRITE, requires_confirmation=True)

        decision = await guard.review(call("demo.write"), risky, ctx)

        assert not decision.allowed
        assert decision.rule == GuardRule.NEEDS_CONFIRMATION

    async def test_a_confirmed_intent_passes(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        proposed = call("demo.write", amount=10)
        guard = DeterministicGuard(
            settings=GuardSettings(allow_writes=True),
            store=store,
            confirmed=frozenset({intent_hash(proposed)}),
        )
        risky = spec("demo.write", SideEffect.WRITE, requires_confirmation=True)

        assert (await guard.review(proposed, risky, ctx)).allowed

    async def test_confirming_one_intent_does_not_confirm_another(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        """Approving 'set stage to cerrado' is not approving 'set stage to perdido'."""
        approved = call("demo.write", stage="cerrado")
        guard = DeterministicGuard(
            settings=GuardSettings(allow_writes=True),
            store=store,
            confirmed=frozenset({intent_hash(approved)}),
        )
        risky = spec("demo.write", SideEffect.WRITE, requires_confirmation=True)

        decision = await guard.review(call("demo.write", stage="perdido"), risky, ctx)

        assert not decision.allowed
        assert decision.rule == GuardRule.NEEDS_CONFIRMATION


class TestCeilings:
    async def test_a_turn_runs_out_of_calls(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        guard = DeterministicGuard(
            settings=GuardSettings(max_tool_calls_per_turn=3, loop_repeat_threshold=99),
            store=store,
        )

        allowed = [
            (await guard.review(call("demo.echo", n=n), spec("demo.echo"), ctx)).allowed
            for n in range(5)
        ]

        assert allowed == [True, True, True, False, False]

    async def test_the_turn_ceiling_is_per_request(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        """A new message is a new turn, and gets its own budget."""
        guard = DeterministicGuard(
            settings=GuardSettings(max_tool_calls_per_turn=1, loop_repeat_threshold=99),
            store=store,
        )
        later = ToolContext(
            tenant_id=ctx.tenant_id,
            session_id=ctx.session_id,
            actor_id=ctx.actor_id,
            request_id="a-different-turn",
        )

        assert (await guard.review(call(), spec("demo.echo"), ctx)).allowed
        assert not (await guard.review(call(), spec("demo.echo"), ctx)).allowed
        assert (await guard.review(call(), spec("demo.echo"), later)).allowed

    async def test_writes_run_out_for_the_session(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        guard = DeterministicGuard(
            settings=GuardSettings(
                allow_writes=True,
                max_actions_per_session_hour=2,
                max_tool_calls_per_turn=99,
                loop_repeat_threshold=99,
            ),
            store=store,
        )
        write = spec("demo.write", SideEffect.WRITE)

        allowed = [
            (await guard.review(call("demo.write", n=n), write, ctx)).allowed for n in range(4)
        ]

        assert allowed == [True, True, False, False]

    async def test_reads_do_not_consume_the_action_ceiling(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        guard = DeterministicGuard(
            settings=GuardSettings(
                allow_writes=True,
                max_actions_per_session_hour=1,
                max_tool_calls_per_turn=99,
                loop_repeat_threshold=99,
            ),
            store=store,
        )

        for n in range(5):
            assert (await guard.review(call("demo.echo", n=n), spec("demo.echo"), ctx)).allowed
        assert (
            await guard.review(call("demo.write"), spec("demo.write", SideEffect.WRITE), ctx)
        ).allowed


class TestLoopDetection:
    async def test_the_same_call_three_times_trips(
        self, guard: DeterministicGuard, ctx: ToolContext
    ) -> None:
        results = [(await guard.review(call(), spec("demo.echo"), ctx)).allowed for _ in range(3)]

        assert results == [True, True, False]

    async def test_it_reports_itself(self, guard: DeterministicGuard, ctx: ToolContext) -> None:
        for _ in range(2):
            await guard.review(call(), spec("demo.echo"), ctx)

        assert (await guard.review(call(), spec("demo.echo"), ctx)).rule == GuardRule.LOOP_DETECTED

    async def test_varying_calls_do_not_trip(
        self, guard: DeterministicGuard, ctx: ToolContext
    ) -> None:
        results = [
            (await guard.review(call(page=n), spec("demo.echo"), ctx)).allowed for n in range(5)
        ]

        assert all(results)

    async def test_the_window_is_per_session(
        self, guard: DeterministicGuard, ctx: ToolContext
    ) -> None:
        other = ToolContext(
            tenant_id=ctx.tenant_id,
            session_id="another-conversation",
            actor_id=ctx.actor_id,
            request_id="r2",
        )
        for _ in range(3):
            await guard.review(call(), spec("demo.echo"), ctx)

        assert (await guard.review(call(), spec("demo.echo"), other)).allowed

    async def test_an_expired_window_forgets(self) -> None:
        """Driven with explicit timestamps: a wall-clock window would be flaky."""
        store = InMemoryGuardStore(loop_window_seconds=60.0)

        counts = [await store.note_intent("s", "fingerprint", 1000.0) for _ in range(3)]
        assert counts == [1, 2, 3]

        # Same intent, well after the window closed. History is gone.
        assert await store.note_intent("s", "fingerprint", 5000.0) == 1

    async def test_a_repeat_just_inside_the_window_still_counts(self) -> None:
        store = InMemoryGuardStore(loop_window_seconds=60.0)

        await store.note_intent("s", "fingerprint", 1000.0)

        assert await store.note_intent("s", "fingerprint", 1059.0) == 2


class TestThroughTheLoop:
    async def test_a_looping_planner_is_stopped_mid_turn(self, registry, ctx) -> None:
        """The end-to-end shape: the guard converts a loop into a REJECTED result."""

        class Stuck:
            async def plan(self, request: PlanRequest) -> Plan:
                return Plan(
                    tool_calls=(ToolCall(id="c", name="demo.echo", arguments={"text": "x"}),)
                )

        agent = Agent(
            registry=registry,
            planner=Stuck(),
            guard=DeterministicGuard(
                settings=GuardSettings(max_tool_calls_per_turn=99), store=InMemoryGuardStore()
            ),
            max_iterations=5,
        )

        reply = await agent.run("go", ctx)

        statuses = [executed.result.status for executed in reply.calls]
        assert statuses[:2] == [ToolStatus.OK, ToolStatus.OK]
        assert statuses[2] is ToolStatus.REJECTED
        assert all(status is ToolStatus.REJECTED for status in statuses[2:])


class TestWriteRetryWithinATurn:
    """Observed in a rehearsal on 19 August: a transient platform error made the
    image generation fail, and the planner cheerfully tried again on its own —
    two paid attempts from one message, with nobody asked."""

    async def test_the_same_write_twice_in_a_turn_is_denied(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        guard = DeterministicGuard(settings=GuardSettings(allow_writes=True), store=store)
        write = spec("demo.generate", SideEffect.WRITE)
        proposed = call("demo.generate", prompt="a house")

        first = await guard.review(proposed, write, ctx)
        second = await guard.review(proposed, write, ctx)

        assert first.allowed
        assert not second.allowed
        assert second.rule == GuardRule.WRITE_ALREADY_ATTEMPTED

    async def test_a_different_write_in_the_same_turn_still_passes(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        """The rule is about repeating one action, not about writing twice."""
        guard = DeterministicGuard(settings=GuardSettings(allow_writes=True), store=store)
        write = spec("demo.generate", SideEffect.WRITE)

        first = await guard.review(call("demo.generate", prompt="a house"), write, ctx)
        second = await guard.review(call("demo.generate", prompt="a boat"), write, ctx)

        assert first.allowed
        assert second.allowed

    async def test_a_new_turn_may_retry_the_same_write(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        """Asking again is a person deciding. That is exactly what should work."""
        guard = DeterministicGuard(settings=GuardSettings(allow_writes=True), store=store)
        write = spec("demo.generate", SideEffect.WRITE)
        proposed = call("demo.generate", prompt="a house")
        later = ToolContext(
            tenant_id=ctx.tenant_id,
            session_id=ctx.session_id,
            actor_id=ctx.actor_id,
            request_id="the-next-message",
        )

        await guard.review(proposed, write, ctx)

        assert (await guard.review(proposed, write, later)).allowed

    async def test_reads_may_repeat_freely_within_a_turn(
        self, store: InMemoryGuardStore, ctx: ToolContext
    ) -> None:
        guard = DeterministicGuard(settings=GuardSettings(), store=store)
        read = spec("demo.echo")
        proposed = call("demo.echo", stage="perdido")

        assert (await guard.review(proposed, read, ctx)).allowed
        assert (await guard.review(proposed, read, ctx)).allowed
