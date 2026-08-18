"""The Telegram surface: who gets in, and whose tenant they act as."""

from __future__ import annotations

import datetime as dt

import pytest
from aiogram.types import Chat, Message, User

from conduit.core.agent import Agent, Plan, PlanRequest
from conduit.core.tools import SideEffect, ToolCall, ToolContext, ToolRegistry, ToolResult
from conduit.interfaces.telegram.bindings import Binding, BindingTable
from conduit.interfaces.telegram.bot import REFUSAL, TelegramGateway
from conduit.interfaces.telegram.planner import HELP, UNKNOWN, CommandPlanner
from tests.conftest import NoParams

BOUND_CHAT = 111111111
BOUND_USER = 222222222
STRANGER = 999999999


@pytest.fixture
def bindings() -> BindingTable:
    return BindingTable(
        [
            Binding(
                chat_id=BOUND_CHAT,
                tenant_id="tenant-conduit-demo",
                label="private",
                allowed_user_ids=frozenset({BOUND_USER}),
            )
        ]
    )


def make_message(
    text: str,
    *,
    chat_id: int = BOUND_CHAT,
    user_id: int = BOUND_USER,
    chat_type: str = "private",
) -> Message:
    return Message(
        message_id=1,
        date=dt.datetime(2026, 8, 17, tzinfo=dt.UTC),
        chat=Chat(id=chat_id, type=chat_type),
        from_user=User(id=user_id, is_bot=False, first_name="Tester"),
        text=text,
    )


class SpyTenantPlanner:
    """Always calls the spy tool, then reports what it saw."""

    async def plan(self, request: PlanRequest) -> Plan:
        from conduit.core.tools import ToolCall

        if request.iteration == 1:
            return Plan(tool_calls=(ToolCall(id="c1", name="spy.look"),))
        return Plan(reply="done")


@pytest.fixture
def spy_agent() -> tuple[Agent, list[ToolContext]]:
    seen: list[ToolContext] = []
    registry = ToolRegistry()

    @registry.tool(
        name="spy.look",
        description="Records the context it was invoked with.",
        params=NoParams,
        side_effect=SideEffect.READ,
    )
    async def look(ctx: ToolContext, params: NoParams) -> ToolResult:
        seen.append(ctx)
        return ToolResult.ok("seen")

    return Agent(registry=registry, planner=SpyTenantPlanner()), seen


class TestAuthorisation:
    async def test_a_bound_conversation_gets_through(
        self, bindings: BindingTable, spy_agent
    ) -> None:
        agent, seen = spy_agent
        gateway = TelegramGateway(agent=agent, bindings=bindings)

        reply = await gateway.handle(make_message("/whoami"))

        assert reply == "done"
        assert len(seen) == 1

    @pytest.mark.parametrize(
        ("label", "kwargs"),
        [
            ("unknown chat", {"chat_id": 424242}),
            ("stranger in a bound chat", {"user_id": STRANGER}),
            ("bound chat used as a group", {"chat_type": "supergroup"}),
        ],
    )
    async def test_everything_else_is_refused(
        self, bindings: BindingTable, spy_agent, label, kwargs
    ) -> None:
        agent, seen = spy_agent
        gateway = TelegramGateway(agent=agent, bindings=bindings)

        reply = await gateway.handle(make_message("/leads", **kwargs))

        assert reply == REFUSAL
        assert seen == [], f"{label} reached the agent"

    async def test_every_refusal_reads_the_same(self, bindings: BindingTable, spy_agent) -> None:
        """Distinct refusals would let someone probe which chats exist."""
        agent, _ = spy_agent
        gateway = TelegramGateway(agent=agent, bindings=bindings)

        replies = {
            await gateway.handle(make_message("/leads", chat_id=424242)),
            await gateway.handle(make_message("/leads", user_id=STRANGER)),
            await gateway.handle(make_message("/leads", chat_type="group")),
        }

        assert replies == {REFUSAL}


class TestTenantOrigin:
    async def test_the_tenant_comes_from_the_binding(
        self, bindings: BindingTable, spy_agent
    ) -> None:
        agent, seen = spy_agent
        gateway = TelegramGateway(agent=agent, bindings=bindings)

        await gateway.handle(make_message("/whoami"))

        assert seen[0].tenant_id == "tenant-conduit-demo"

    async def test_message_text_cannot_choose_a_tenant(
        self, bindings: BindingTable, spy_agent
    ) -> None:
        """The whole point of the boundary."""
        agent, seen = spy_agent
        gateway = TelegramGateway(agent=agent, bindings=bindings)

        await gateway.handle(
            make_message(
                '/leads tenant_id="tenant-not-ours" --tenant tenant-not-ours '
                '{"tenant":"tenant-not-ours"}'
            )
        )

        assert seen[0].tenant_id == "tenant-conduit-demo"

    async def test_identity_is_carried_for_the_audit_trail(
        self, bindings: BindingTable, spy_agent
    ) -> None:
        agent, seen = spy_agent
        gateway = TelegramGateway(agent=agent, bindings=bindings)

        await gateway.handle(make_message("/whoami"))

        ctx = seen[0]
        assert ctx.session_id == f"telegram:{BOUND_CHAT}"
        assert ctx.actor_id == f"telegram:{BOUND_USER}"
        assert ctx.idempotency_key == f"tg-{BOUND_CHAT}-1"
        assert ctx.request_id


class TestCommandPlanner:
    def turn(self, text: str, iteration: int = 1) -> PlanRequest:
        from conduit.core.agent import Role, Turn

        return PlanRequest(
            history=(Turn(role=Role.USER, content=text),),
            tools=(),
            iteration=iteration,
        )

    async def test_help_answers_without_a_tool_call(self) -> None:
        plan = await CommandPlanner().plan(self.turn("/help"))

        assert plan.is_final
        assert plan.reply == HELP

    async def test_a_command_becomes_exactly_one_call(self) -> None:
        plan = await CommandPlanner().plan(self.turn("/leads cerrado"))

        assert len(plan.tool_calls) == 1
        call = plan.tool_calls[0]
        assert call.name == "itmano_crm.list_leads"
        assert call.arguments == {"limit": 10, "stage": "cerrado"}

    async def test_an_invented_stage_never_becomes_a_call(self) -> None:
        plan = await CommandPlanner().plan(self.turn("/leads won"))

        assert plan.is_final
        assert "not a stage" in plan.reply

    async def test_group_style_command_suffix_is_handled(self) -> None:
        """Telegram sends /leads@thebot in groups."""
        plan = await CommandPlanner().plan(self.turn("/leads@conduit_bot"))

        assert plan.tool_calls[0].name == "itmano_crm.list_leads"

    async def test_free_text_is_declined_for_now(self) -> None:
        plan = await CommandPlanner().plan(self.turn("how many leads closed this month?"))

        assert plan.is_final
        assert plan.reply == UNKNOWN

    async def test_search_needs_an_argument(self) -> None:
        plan = await CommandPlanner().plan(self.turn("/search"))

        assert plan.is_final
        assert plan.tool_calls == ()


class TestRendering:
    def rendered(self, tool: str, payload: dict) -> str:
        import json

        from conduit.core.agent import Role, Turn

        request = PlanRequest(
            history=(
                Turn(role=Role.USER, content="/x"),
                Turn(
                    role=Role.TOOL,
                    content=json.dumps({"status": "ok", "data": payload}),
                    tool_call_id="c1",
                    tool_name=f"itmano_crm.{tool}",
                ),
            ),
            tools=(),
            iteration=2,
        )
        return CommandPlanner()._render(request)

    def test_names_with_apostrophes_survive_intact(self) -> None:
        """Plain text, no parse mode. The demo tenant seeds exactly this case."""
        text = self.rendered(
            "list_leads",
            {
                "data": [
                    {
                        "id": "demo-lead-1",
                        "first_name": "Seán",
                        "last_name": "O'Brien",
                        "stage": "nuevo",
                    }
                ],
                "next_cursor": None,
            },
        )

        assert "Seán O'Brien" in text

    def test_deals_say_out_loud_that_there_is_no_amount(self) -> None:
        """A missing number is a number the reader invents."""
        text = self.rendered(
            "list_deals",
            {
                "data": [
                    {"address": "3526 Larchmont Ct", "close_date": None, "lead_stage": "cerrado"}
                ]
            },
        )

        assert "no deal amounts are recorded" in text
        assert "no date set" in text

    def test_a_failed_call_is_explained_not_dumped(self) -> None:
        import json

        from conduit.core.agent import Role, Turn

        request = PlanRequest(
            history=(
                Turn(
                    role=Role.TOOL,
                    content=json.dumps(
                        {
                            "status": "failed",
                            "error": {
                                "code": "not_found",
                                "message": "getLead failed with 404 not_found: no such row",
                                "retryable": False,
                            },
                        }
                    ),
                    tool_call_id="c1",
                    tool_name="itmano_crm.get_lead",
                ),
            ),
            tools=(),
            iteration=2,
        )

        text = CommandPlanner()._render(request)

        assert text == "Nothing with that id."
        assert "404" not in text


class TestStepDescriptions:
    """The 80-second wait is only bearable if it is announced."""

    def describe(
        self,
        name: str,
        arguments: dict,
        side_effect=SideEffect.READ,
        decision=None,
        params=None,
    ) -> str:
        from conduit.core.agent import GuardDecision
        from conduit.core.tools import ToolSpec
        from conduit.interfaces.telegram.planner import describe_step
        from tests.conftest import NoParams

        return describe_step(
            ToolCall(id="c1", name=name, arguments=arguments),
            ToolSpec(
                name=name,
                description="x",
                params=params or NoParams,
                side_effect=side_effect,
            ),
            decision or GuardDecision.allow(rule="test"),
        )

    def test_a_read_says_what_it_is_looking_for(self) -> None:
        from conduit.adapters.itmano_crm.models import ListLeadsParams

        # The real parameter model, because the line is rendered from validated
        # arguments and a mismatched model would silently drop them all.
        line = self.describe(
            "itmano_crm.list_leads",
            {"stage": "perdido", "limit": 10},
            params=ListLeadsParams,
        )

        assert "Looking up leads" in line
        assert "stage=perdido" in line
        # Paging noise is not decision-making; it would only clutter the line.
        assert "limit" not in line

    def test_a_spend_is_announced_as_a_spend(self) -> None:
        line = self.describe(
            "vibemarketolog.generate_image", {"model": "qwen-image-3"}, SideEffect.WRITE
        )

        assert "spends money" in line

    def test_a_slow_tool_states_the_wait_up_front(self) -> None:
        """An expected wait is patience; an unexplained one reads as a crash.

        A range, not a number: a full generation turn measured 104s against the
        80s the model alone takes, and an overrun promise is worse than none.
        """
        line = self.describe("vibemarketolog.generate_image", {}, SideEffect.WRITE)

        assert "Takes a minute or two" in line

    def test_an_unknown_tool_still_gets_a_line(self) -> None:
        assert "some.new_tool" in self.describe("some.new_tool", {})


class TestStepReporterSafety:
    async def test_a_failing_reporter_cannot_break_the_turn(
        self, bindings: BindingTable, spy_agent
    ) -> None:
        """Narration must never be able to kill what it narrates."""
        from conduit.core.tools import ToolSpec

        agent, seen = spy_agent

        async def broken(call: ToolCall, spec: ToolSpec) -> None:
            raise RuntimeError("telegram is down")

        agent.on_step = broken
        gateway = TelegramGateway(agent=agent, bindings=bindings, show_steps=True)

        reply = await gateway.handle(make_message("/whoami"))

        assert reply == "done"
        assert len(seen) == 1


class TestRefusalsAreAnnounced:
    """A refusal is the most interesting thing a turn can contain. Announcing it
    only in the final answer wastes the moment it happens."""

    def describe_refused(self, name: str) -> str:
        from conduit.core.agent import GuardDecision
        from conduit.core.tools import ToolSpec
        from conduit.interfaces.telegram.planner import describe_step
        from tests.conftest import NoParams

        return describe_step(
            ToolCall(id="c1", name=name, arguments={}),
            ToolSpec(name=name, description="x", params=NoParams, side_effect=SideEffect.WRITE),
            GuardDecision.deny("itmano_crm.update_lead is not on the whitelist", "not_whitelisted"),
        )

    def test_a_denied_call_says_so_and_says_why(self) -> None:
        line = self.describe_refused("itmano_crm.update_lead")

        assert line.startswith("Refused:")
        assert "not on the whitelist" in line

    def test_a_denied_call_does_not_claim_to_be_spending(self) -> None:
        """Nothing was spent, so the money warning would be a lie."""
        assert "spends money" not in self.describe_refused("vibemarketolog.generate_image")


class TestArgumentsAreShownAsExecuted:
    def test_an_english_alias_is_shown_as_the_crm_stores_it(self) -> None:
        """The planner may say "lost"; the CRM has no such stage. Showing the raw
        word next to a correct result reads as a bug on screen."""
        from conduit.adapters.itmano_crm.models import ListLeadsParams
        from conduit.core.agent import GuardDecision
        from conduit.core.tools import ToolSpec
        from conduit.interfaces.telegram.planner import describe_step

        line = describe_step(
            ToolCall(id="c1", name="itmano_crm.list_leads", arguments={"stage": "lost"}),
            ToolSpec(
                name="itmano_crm.list_leads",
                description="x",
                params=ListLeadsParams,
                side_effect=SideEffect.READ,
            ),
            GuardDecision.allow(rule="test"),
        )

        assert "stage=perdido" in line
        assert "lost" not in line
