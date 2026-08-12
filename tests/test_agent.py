"""The orchestration loop's ordering guarantees."""

from __future__ import annotations

from collections import deque
from collections.abc import Iterable

from conduit.core.agent import (
    Agent,
    AuditEvent,
    AuditPhase,
    GuardDecision,
    Plan,
    PlanRequest,
    ReadOnlyGuard,
    Role,
    StopReason,
    Turn,
)
from conduit.core.tools import (
    SideEffect,
    ToolCall,
    ToolContext,
    ToolRegistry,
    ToolResult,
    ToolSpec,
    ToolStatus,
)
from tests.conftest import NoParams


class ScriptedPlanner:
    """Emits a fixed sequence of plans, one per iteration."""

    def __init__(self, plans: Iterable[Plan]) -> None:
        self.plans = deque(plans)
        self.requests: list[PlanRequest] = []

    async def plan(self, request: PlanRequest) -> Plan:
        self.requests.append(request)
        if not self.plans:
            return Plan(reply="done")
        return self.plans.popleft()


class ExplodingPlanner:
    async def plan(self, request: PlanRequest) -> Plan:
        raise RuntimeError("model unreachable")


class RecordingAudit:
    def __init__(self) -> None:
        self.events: list[AuditEvent] = []

    async def record(self, event: AuditEvent) -> None:
        self.events.append(event)


class PermissiveGuard:
    async def review(self, call: ToolCall, spec: ToolSpec, ctx: ToolContext) -> GuardDecision:
        return GuardDecision.allow(rule="test")


class TestTerminating:
    async def test_a_plan_without_calls_ends_the_turn(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        agent = Agent(registry=registry, planner=ScriptedPlanner([Plan(reply="hello")]))

        reply = await agent.run("hi", ctx)

        assert reply.stop_reason is StopReason.COMPLETED
        assert reply.text == "hello"
        assert reply.calls == ()

    async def test_history_is_carried_into_the_transcript(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        planner = ScriptedPlanner([Plan(reply="ok")])
        agent = Agent(registry=registry, planner=planner)
        earlier = [Turn(role=Role.USER, content="previous")]

        reply = await agent.run("now", ctx, history=earlier)

        assert [turn.content for turn in reply.transcript] == ["previous", "now", "ok"]

    async def test_the_loop_stops_at_max_iterations(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        looping = Plan(tool_calls=(ToolCall(id="c", name="demo.echo", arguments={"text": "x"}),))
        agent = Agent(
            registry=registry,
            planner=ScriptedPlanner([looping] * 10),
            guard=PermissiveGuard(),
            max_iterations=3,
        )

        reply = await agent.run("go", ctx)

        assert reply.stop_reason is StopReason.MAX_ITERATIONS
        assert len(reply.calls) == 3

    async def test_a_failing_planner_is_reported_not_raised(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        agent = Agent(registry=registry, planner=ExplodingPlanner())

        reply = await agent.run("go", ctx)

        assert reply.stop_reason is StopReason.PLANNER_FAILED
        assert "model unreachable" in reply.error


class TestExecution:
    async def test_a_tool_result_is_fed_back_to_the_planner(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        planner = ScriptedPlanner(
            [
                Plan(tool_calls=(ToolCall(id="c1", name="demo.echo", arguments={"text": "pong"}),)),
                Plan(reply="the tool said pong"),
            ]
        )
        agent = Agent(registry=registry, planner=planner, guard=PermissiveGuard())

        reply = await agent.run("ping", ctx)

        assert reply.stop_reason is StopReason.COMPLETED
        tool_turns = [turn for turn in reply.transcript if turn.role is Role.TOOL]
        assert len(tool_turns) == 1
        assert tool_turns[0].tool_call_id == "c1"
        assert "pong" in tool_turns[0].content
        # The second planner call must have seen that turn.
        assert any(turn.role is Role.TOOL for turn in planner.requests[1].history)

    async def test_an_unknown_tool_is_rejected_without_reaching_the_guard(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        audit = RecordingAudit()
        agent = Agent(
            registry=registry,
            planner=ScriptedPlanner(
                [Plan(tool_calls=(ToolCall(id="c1", name="demo.ghost"),)), Plan(reply="oh")]
            ),
            guard=PermissiveGuard(),
            audit=audit,
        )

        reply = await agent.run("go", ctx)

        assert reply.calls[0].result.status is ToolStatus.REJECTED
        assert audit.events == []


class TestGuardOrdering:
    async def test_writes_are_denied_by_the_default_guard(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        agent = Agent(
            registry=registry,
            planner=ScriptedPlanner(
                [Plan(tool_calls=(ToolCall(id="c1", name="demo.write_thing"),)), Plan(reply="no")]
            ),
            guard=ReadOnlyGuard(),
        )

        reply = await agent.run("write it", ctx)

        assert reply.calls[0].decision.allowed is False
        assert reply.calls[0].result.status is ToolStatus.REJECTED

    async def test_a_denied_call_never_runs_its_handler(self, ctx: ToolContext) -> None:
        reg = ToolRegistry()
        ran: list[str] = []

        @reg.tool(
            name="demo.dangerous",
            description="Must not run.",
            params=NoParams,
            side_effect=SideEffect.WRITE,
        )
        async def dangerous(ctx: ToolContext, params: NoParams) -> ToolResult:
            ran.append("yes")
            return ToolResult.ok()

        agent = Agent(
            registry=reg,
            planner=ScriptedPlanner(
                [Plan(tool_calls=(ToolCall(id="c1", name="demo.dangerous"),)), Plan(reply="no")]
            ),
            guard=ReadOnlyGuard(),
        )

        await agent.run("do it", ctx)

        assert ran == []


class TestAudit:
    async def test_intent_is_recorded_before_the_outcome(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        audit = RecordingAudit()
        agent = Agent(
            registry=registry,
            planner=ScriptedPlanner(
                [
                    Plan(
                        tool_calls=(ToolCall(id="c1", name="demo.echo", arguments={"text": "x"}),)
                    ),
                    Plan(reply="ok"),
                ]
            ),
            guard=PermissiveGuard(),
            audit=audit,
        )

        await agent.run("go", ctx)

        assert [event.phase for event in audit.events] == [AuditPhase.INTENT, AuditPhase.OUTCOME]
        intent, outcome = audit.events
        assert intent.status is None
        assert intent.tool_name == "demo.echo"
        assert intent.tenant_id == "tenant-demo"
        assert intent.side_effect is SideEffect.READ
        assert outcome.status is ToolStatus.OK

    async def test_a_denied_call_is_still_audited(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        audit = RecordingAudit()
        agent = Agent(
            registry=registry,
            planner=ScriptedPlanner(
                [Plan(tool_calls=(ToolCall(id="c1", name="demo.write_thing"),)), Plan(reply="no")]
            ),
            guard=ReadOnlyGuard(),
            audit=audit,
        )

        await agent.run("write it", ctx)

        assert [event.phase for event in audit.events] == [AuditPhase.INTENT, AuditPhase.OUTCOME]
        assert audit.events[0].allowed is False
        assert audit.events[1].status is ToolStatus.REJECTED
