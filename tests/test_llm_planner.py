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


class TestDegradation:
    """The safety net: if the model API is down, commands must still answer."""

    @respx.mock
    async def test_commands_never_touch_the_model(self, planner: LlmPlanner) -> None:
        from conduit.interfaces.telegram.planner import CommandFastPath

        route = respx.post(f"{BASE}/generate").mock(side_effect=httpx.ConnectError("down"))
        fast_path = CommandFastPath(fallback=planner)

        plan = await fast_path.plan(request_for("/leads cerrado"))

        assert route.call_count == 0
        assert plan.tool_calls[0].name == "itmano_crm.list_leads"

    @respx.mock
    async def test_free_text_degrades_to_a_sentence_not_a_crash(self, planner: LlmPlanner) -> None:
        from conduit.interfaces.telegram.planner import CommandFastPath

        respx.post(f"{BASE}/generate").mock(side_effect=httpx.ConnectError("down"))
        fast_path = CommandFastPath(fallback=planner)

        plan = await fast_path.plan(request_for("cuantos leads hay?"))

        assert plan.reply == FAILED_REPLY
        assert "/help" in plan.reply


class TestParameterNotesReachThePlanner:
    """Field descriptions used to be dropped from the prompt entirely.

    Only the tool-level sentence was rendered, so every rule written on an
    individual argument — which image model to pay for, that an owner id must be
    real, that a cursor only works with its own filters — never reached the
    model. The visible symptom was the planner picking the cheapest image model
    for a poster that needed legible text, no matter how the rule was worded.
    """

    def test_argument_descriptions_are_rendered(self) -> None:
        spec = ToolSpec(
            name="demo.echo",
            description="Repeat text.",
            params=EchoParams,
            side_effect=SideEffect.READ,
        )

        prompt = build_system_prompt((spec,))

        assert "Repeat text." in prompt
        assert "text:" in prompt

    def test_a_field_note_survives_into_the_prompt(self) -> None:
        from pydantic import BaseModel, Field

        class Documented(BaseModel):
            choice: str = Field(description="Pick the expensive one when it matters.")

        spec = ToolSpec(
            name="demo.documented",
            description="A tool.",
            params=Documented,
            side_effect=SideEffect.READ,
        )

        assert "Pick the expensive one when it matters." in build_system_prompt((spec,))


class TestReplyLanguage:
    """Decided in code, not left to a rule in a cached prompt.

    Three live failures forced this: an English question answered in Spanish
    because every value in the result was Spanish, and another answered in
    Russian because a tool description happened to mention Russian.
    """

    def test_it_places_the_three_languages_this_deployment_sees(self) -> None:
        from conduit.adapters.vibemarketolog.planner import detect_language

        assert detect_language("show me the leads in the lost stage") == "English"
        assert detect_language("muéstrame los leads en etapa perdido") == "Spanish"
        assert detect_language("покажи мне лиды на этапе perdido") == "Russian"

    def test_one_ambiguous_word_is_not_enough_for_spanish(self) -> None:
        """'leads' and 'en' occur in English too; a single hit proves nothing."""
        from conduit.adapters.vibemarketolog.planner import detect_language

        assert detect_language("show me the leads") == "English"

    def test_an_empty_message_names_no_language(self) -> None:
        from conduit.adapters.vibemarketolog.planner import detect_language

        assert detect_language("   ") is None

    def test_the_instruction_is_the_last_thing_the_model_reads(self) -> None:
        from conduit.adapters.vibemarketolog.planner import _transcript

        request = PlanRequest(
            history=(
                Turn(role=Role.USER, content="show me the leads in the lost stage"),
                Turn(
                    role=Role.TOOL,
                    content='{"stage":"perdido"}',
                    tool_call_id="c1",
                    tool_name="itmano_crm.list_leads",
                ),
            ),
            tools=(),
            iteration=2,
        )

        assert _transcript(request).endswith("Write your reply in English.")

    def test_the_tool_descriptions_name_no_language(self) -> None:
        """A description saying "in English or Russian" seeded Russian replies to
        English questions, once the argument notes started reaching the model."""
        from conduit.adapters.vibemarketolog.tools import GenerateImageParams

        schema = GenerateImageParams.model_json_schema()
        prompt_note = schema["properties"]["prompt"]["description"]

        assert "Russian" not in prompt_note
        assert "English" not in prompt_note
