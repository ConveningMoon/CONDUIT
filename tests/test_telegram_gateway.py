"""The Telegram surface: who gets in, and whose tenant they act as."""

from __future__ import annotations

import datetime as dt

import pytest
from aiogram.types import Chat, Message, User

from conduit.core.agent import Agent, Plan, PlanRequest
from conduit.core.tools import SideEffect, ToolContext, ToolRegistry, ToolResult
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
            make_message('/leads tenant_id="tenant-aj" --tenant tenant-aj {"tenant":"tenant-aj"}')
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
