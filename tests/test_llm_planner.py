"""The planner's parser, offline.

Without native function calling the model returns a string, so parsing is the
load-bearing part. These cost nothing to run; the golden set costs money and
lives in `scripts/run_planner_evals.py`.
"""

from __future__ import annotations

import httpx
import pytest
import respx
from pydantic import SecretStr

from conduit.adapters.vibemarketolog import (
    FAILED_REPLY,
    LlmPlanner,
    VibemarketologClient,
    VibemarketologSettings,
    build_system_prompt,
)
from conduit.adapters.vibemarketolog.planner import LlmPlanner as Planner
from conduit.core.agent import PlanRequest, Role, Turn
from conduit.core.telemetry import turn_ledger
from conduit.core.tools import SideEffect, ToolRegistry, ToolSpec
from tests.conftest import EchoParams, NoParams

BASE = "https://platform.test/api/agent"
KNOWN = frozenset({"itmano_crm.list_leads", "itmano_crm.get_lead"})


def parse(text: str):
    return Planner._parse(text, KNOWN)


@pytest.fixture
def settings() -> VibemarketologSettings:
    return VibemarketologSettings(base_url=BASE, api_key=SecretStr("oc_test"))


@pytest.fixture
async def planner(settings: VibemarketologSettings):
    async with VibemarketologClient(settings) as client:
        yield LlmPlanner(client=client, known_tools=KNOWN)


def request_for(text: str) -> PlanRequest:
    return PlanRequest(history=(Turn(role=Role.USER, content=text),), tools=(), iteration=1)


def completion(text: str, cost: float = 0.5) -> httpx.Response:
    return httpx.Response(
        200,
        json={"text": text, "cost": cost, "usage": {"input": 100, "output": 20}},
    )


class TestParsing:
    def test_a_clean_plan_parses(self) -> None:
        output = parse('{"reply":"","tool_calls":[{"id":"1","name":"itmano_crm.list_leads"}]}')

        assert output.tool_calls[0].name == "itmano_crm.list_leads"

    def test_markdown_fences_are_tolerated(self) -> None:
        """Models wrap JSON in fences constantly, whatever the instructions say."""
        output = parse('```json\n{"reply":"hola","tool_calls":[]}\n```')

        assert output.reply == "hola"

    def test_a_reply_with_no_calls_is_valid(self) -> None:
        assert parse('{"reply":"no puedo hacer eso","tool_calls":[]}').reply

    def test_prose_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="not valid JSON"):
            parse("Claro, voy a buscar los leads para ti.")

    def test_an_empty_reply_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="empty"):
            parse("   ")

    def test_a_json_array_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="object"):
            parse('[{"name":"itmano_crm.list_leads"}]')

    def test_a_hallucinated_tool_is_rejected(self) -> None:
        """Code catches this, not the model's good behaviour."""
        with pytest.raises(ValueError, match="no such tool"):
            parse('{"tool_calls":[{"id":"1","name":"itmano_crm.delete_everything"}]}')

    def test_neither_reply_nor_call_is_rejected(self) -> None:
        with pytest.raises(ValueError, match="neither"):
            parse('{"reply":"","tool_calls":[]}')

    def test_unknown_fields_are_ignored(self) -> None:
        """A model adding commentary keys should not fail the whole plan."""
        output = parse(
            '{"reply":"","thinking":"hmm","tool_calls":'
            '[{"id":"1","name":"itmano_crm.get_lead","arguments":{"id":"x"},"why":"because"}]}'
        )

        assert output.tool_calls[0].arguments == {"id": "x"}


class TestSystemPrompt:
    def test_enums_reach_the_prompt(self) -> None:
        """If the valid values are not in the prompt the model has to guess."""
        registry = ToolRegistry()
        spec = ToolSpec(
            name="demo.echo",
            description="Repeat text.",
            params=EchoParams,
            side_effect=SideEffect.READ,
        )
        registry.register(spec, lambda ctx, params: None)  # type: ignore[arg-type]

        prompt = build_system_prompt((spec,))

        assert "demo.echo" in prompt
        assert "text" in prompt
        assert "Repeat text." in prompt

    def test_optional_arguments_are_marked(self) -> None:
        spec = ToolSpec(
            name="demo.echo",
            description="Repeat text.",
            params=EchoParams,
            side_effect=SideEffect.READ,
        )

        prompt = build_system_prompt((spec,))

        assert "times?" in prompt


class TestRetry:
    @respx.mock
    async def test_one_bad_reply_is_repaired(self, planner: LlmPlanner) -> None:
        route = respx.post(f"{BASE}/generate").mock(
            side_effect=[
                completion("Sure! Here you go."),
                completion('{"reply":"","tool_calls":[{"id":"1","name":"itmano_crm.list_leads"}]}'),
            ]
        )

        with turn_ledger() as ledger:
            plan = await planner.plan(request_for("leads"))

        assert plan.tool_calls[0].name == "itmano_crm.list_leads"
        assert route.call_count == 2
        assert [entry.retry for entry in ledger] == [False, True]

    @respx.mock
    async def test_the_retry_is_capped_at_one(self, planner: LlmPlanner) -> None:
        """An unbounded repair loop is a hole in the cost ceiling."""
        route = respx.post(f"{BASE}/generate").mock(
            return_value=completion("still not JSON, sorry")
        )

        plan = await planner.plan(request_for("leads"))

        assert route.call_count == 2
        assert plan.is_final
        assert plan.reply == FAILED_REPLY

    @respx.mock
    async def test_a_dead_api_answers_a_human_sentence(self, planner: LlmPlanner) -> None:
        respx.post(f"{BASE}/generate").mock(side_effect=httpx.ConnectError("down"))

        plan = await planner.plan(request_for("leads"))

        assert plan.reply == FAILED_REPLY
        assert plan.is_final

    @respx.mock
    async def test_an_api_error_does_not_burn_a_retry(self, planner: LlmPlanner) -> None:
        """A 500 is not a parse problem; repeating the same prompt will not fix it."""
        route = respx.post(f"{BASE}/generate").mock(return_value=httpx.Response(500, text="boom"))

        await planner.plan(request_for("leads"))

        assert route.call_count == 1


class TestTelemetry:
    @respx.mock
    async def test_every_call_is_recorded_with_its_cost(self, planner: LlmPlanner) -> None:
        respx.post(f"{BASE}/generate").mock(
            return_value=completion('{"reply":"hola","tool_calls":[]}', cost=0.5)
        )

        with turn_ledger() as ledger:
            await planner.plan(request_for("hola"))

        assert len(ledger) == 1
        assert ledger[0].cost_rub == 0.5
        assert ledger[0].model == "gpt-5.6-luna"
        assert ledger[0].input_tokens == 100

    @respx.mock
    async def test_ledgers_do_not_leak_between_turns(self, planner: LlmPlanner) -> None:
        respx.post(f"{BASE}/generate").mock(
            return_value=completion('{"reply":"hola","tool_calls":[]}')
        )

        with turn_ledger() as first:
            await planner.plan(request_for("uno"))
        with turn_ledger() as second:
            await planner.plan(request_for("dos"))

        assert len(first) == 1
        assert len(second) == 1


class TestNoParamsTool:
    def test_a_tool_without_arguments_renders(self) -> None:
        spec = ToolSpec(
            name="demo.ping",
            description="Ping.",
            params=NoParams,
            side_effect=SideEffect.READ,
        )

        assert "demo.ping()" in build_system_prompt((spec,))


class TestResultClipping:
    def test_a_normal_page_reaches_the_planner_whole(self) -> None:
        """A page of ten leads is ~3000 chars. Cutting it was the truncation bug."""
        from conduit.adapters.vibemarketolog.planner import _clip

        page = "x" * 3105

        assert _clip(page) == page

    def test_an_oversized_result_says_it_was_cut(self) -> None:
        """Silent truncation makes the model invent the rest or hedge blindly."""
        from conduit.adapters.vibemarketolog.planner import MAX_RESULT_CHARS, _clip

        clipped = _clip("x" * (MAX_RESULT_CHARS + 500))

        assert "truncated: 500 more characters" in clipped
        assert clipped.startswith("x" * 100)
