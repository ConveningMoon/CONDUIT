"""Generation tools, offline.

Every response here is simulated. Real generation costs rubles, so the code has
to be right before a single call leaves the process.
"""

from __future__ import annotations

import httpx
import pytest
import respx
from pydantic import SecretStr, ValidationError

from conduit.adapters.vibemarketolog import VibemarketologClient, VibemarketologSettings
from conduit.adapters.vibemarketolog.tools import GenerateImageParams, register
from conduit.adapters.vibemarketolog.tools import _first_url as first_url
from conduit.core.guard import DeterministicGuard, GuardSettings, InMemoryGuardStore
from conduit.core.tools import (
    SideEffect,
    ToolCall,
    ToolContext,
    ToolErrorCode,
    ToolRegistry,
    ToolStatus,
)

BASE = "https://platform.test/api/agent"


@pytest.fixture
async def client():
    settings = VibemarketologSettings(
        base_url=BASE, api_key=SecretStr("oc_test"), image_model="z-image"
    )
    async with VibemarketologClient(settings) as instance:
        yield instance


@pytest.fixture
def registry(client: VibemarketologClient) -> ToolRegistry:
    reg = ToolRegistry()
    register(reg, client)
    return reg


class TestSideEffects:
    def test_generating_is_a_write(self, registry: ToolRegistry) -> None:
        """A rouble spent does not come back. That is what WRITE is for."""
        assert registry.spec("vibemarketolog.generate_image").side_effect is SideEffect.WRITE

    def test_estimating_is_a_read(self, registry: ToolRegistry) -> None:
        assert registry.spec("vibemarketolog.estimate_generation").side_effect is SideEffect.READ

    def test_there_is_no_video_tool(self, registry: ToolRegistry) -> None:
        """A clip is 149-590 RUB. Pricing is exposed; spending is not."""
        assert {spec.name for spec in registry.specs()} == {
            "vibemarketolog.generate_image",
            "vibemarketolog.estimate_generation",
        }

    def test_the_description_warns_that_it_spends(self, registry: ToolRegistry) -> None:
        description = registry.spec("vibemarketolog.generate_image").description

        assert "SPENDS MONEY" in description

    async def test_the_guard_can_allow_generation_while_refusing_crm_writes(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        """The demo posture: every read, plus exactly one chosen write."""
        guard = DeterministicGuard(
            settings=GuardSettings(
                allow_writes=True,
                whitelist=frozenset(
                    {"vibemarketolog.generate_image", "vibemarketolog.estimate_generation"}
                ),
            ),
            store=InMemoryGuardStore(),
        )
        image = registry.spec("vibemarketolog.generate_image")

        allowed = await guard.review(ToolCall(id="c1", name=image.name, arguments={}), image, ctx)
        refused = await guard.review(
            ToolCall(id="c2", name="itmano_crm.update_lead", arguments={}),
            registry.spec("vibemarketolog.generate_image").model_copy(
                update={"name": "itmano_crm.update_lead"}
            ),
            ctx,
        )

        assert allowed.allowed
        assert not refused.allowed
        assert refused.rule == "not_whitelisted"


class TestEstimating:
    @respx.mock
    async def test_a_video_price_comes_back_without_charging(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        respx.post(f"{BASE}/generate/estimate").mock(
            return_value=httpx.Response(
                200,
                json={
                    "valid": True,
                    "model": "veo3_fast",
                    "reserve_rub": 149.0,
                    "balance": {"after_reserve": 346.0},
                },
            )
        )

        result = await registry.invoke(
            ToolCall(
                id="c1",
                name="vibemarketolog.estimate_generation",
                arguments={"media_type": "video", "prompt": "a house tour"},
            ),
            ctx,
        )

        assert result.status is ToolStatus.OK
        assert isinstance(result.data, dict)
        assert result.data["price_rub"] == 149.0
        assert result.data["charged"] is False

    @respx.mock
    async def test_estimating_never_calls_generate(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        respx.post(f"{BASE}/generate/estimate").mock(
            return_value=httpx.Response(200, json={"valid": True, "reserve_rub": 7.0})
        )
        generate = respx.post(f"{BASE}/generate").mock(return_value=httpx.Response(200, json={}))

        await registry.invoke(
            ToolCall(
                id="c1",
                name="vibemarketolog.estimate_generation",
                arguments={"media_type": "image", "prompt": "a house"},
            ),
            ctx,
        )

        assert not generate.called


class TestGenerating:
    @respx.mock
    async def test_the_happy_path_polls_until_ready(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        respx.post(f"{BASE}/generate").mock(return_value=httpx.Response(200, json={"id": "gen-1"}))
        respx.get(f"{BASE}/generation/gen-1/status").mock(
            side_effect=[
                httpx.Response(200, json={"status": "processing"}),
                httpx.Response(
                    200,
                    json={"status": "done", "url": "https://cdn.test/a.png", "cost": 1.2},
                ),
            ]
        )

        result = await registry.invoke(
            ToolCall(
                id="c1",
                name="vibemarketolog.generate_image",
                arguments={"prompt": "a bright coastal house at sunset"},
            ),
            ctx,
        )

        assert result.status is ToolStatus.OK
        assert isinstance(result.data, dict)
        assert result.data["url"] == "https://cdn.test/a.png"
        assert result.data["cost_rub"] == 1.2

    @respx.mock
    async def test_strict_is_always_sent(self, registry: ToolRegistry, ctx: ToolContext) -> None:
        """strict=true rejects bad params before the debit, not after."""
        import json

        start = respx.post(f"{BASE}/generate").mock(
            return_value=httpx.Response(200, json={"id": "gen-1"})
        )
        respx.get(f"{BASE}/generation/gen-1/status").mock(
            return_value=httpx.Response(200, json={"status": "done", "url": "https://x/y.png"})
        )

        await registry.invoke(
            ToolCall(
                id="c1",
                name="vibemarketolog.generate_image",
                arguments={"prompt": "a house"},
            ),
            ctx,
        )

        assert json.loads(start.calls.last.request.content)["strict"] is True

    @respx.mock
    async def test_a_failed_generation_is_a_result_not_an_exception(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        respx.post(f"{BASE}/generate").mock(return_value=httpx.Response(200, json={"id": "g"}))
        respx.get(f"{BASE}/generation/g/status").mock(
            return_value=httpx.Response(200, json={"status": "failed", "error": "nsfw"})
        )

        result = await registry.invoke(
            ToolCall(
                id="c1",
                name="vibemarketolog.generate_image",
                arguments={"prompt": "a house"},
            ),
            ctx,
        )

        assert result.status is ToolStatus.FAILED
        assert result.error is not None
        assert "nsfw" in result.error.message

    @respx.mock
    async def test_a_rejected_request_never_reaches_polling(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        respx.post(f"{BASE}/generate").mock(
            return_value=httpx.Response(422, text="prompt too long")
        )
        status = respx.get(url__regex=rf"{BASE}/generation/.*").mock(
            return_value=httpx.Response(200, json={})
        )

        result = await registry.invoke(
            ToolCall(
                id="c1",
                name="vibemarketolog.generate_image",
                arguments={"prompt": "a house"},
            ),
            ctx,
        )

        assert result.error is not None
        assert result.error.code is ToolErrorCode.INVALID_ARGUMENTS
        assert not status.called


class TestArguments:
    def test_an_overlong_prompt_is_refused_locally(self) -> None:
        """The catalogue rejects over 800 characters. Better to never send it."""
        with pytest.raises(ValidationError):
            GenerateImageParams(prompt="x" * 801)

    def test_an_invented_aspect_ratio_is_refused(self) -> None:
        with pytest.raises(ValidationError):
            GenerateImageParams(prompt="a house", aspect_ratio="7:3")  # type: ignore[arg-type]


class TestUrlExtraction:
    @pytest.mark.parametrize(
        "payload",
        [
            {"url": "https://x/a.png"},
            {"result_url": "https://x/a.png"},
            {"urls": ["https://x/a.png"]},
            {"files": [{"url": "https://x/a.png"}]},
            {"result": {"url": "https://x/a.png"}},
            {"result_object": {"images": [{"file_url": "https://x/a.png"}]}},
        ],
    )
    def test_the_url_is_found_whatever_shape_it_arrives_in(self, payload: dict) -> None:
        """The catalogue documents several conventions. Look, do not guess."""
        assert first_url(payload) == "https://x/a.png"

    def test_a_reply_with_no_file_yields_none(self) -> None:
        assert first_url({"status": "done"}) is None


class TestTerminalStates:
    """Cost 1.20 RUB and 180 seconds to learn: the API says 'complete', not
    'completed' or 'done'."""

    @respx.mock
    async def test_the_real_terminal_word_is_recognised(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        respx.post(f"{BASE}/generate").mock(return_value=httpx.Response(200, json={"id": "g"}))
        respx.get(f"{BASE}/generation/g/status").mock(
            return_value=httpx.Response(
                200,
                json={
                    "status": "complete",
                    "result_url": "https://x/y.png",
                    "cost": 1.2,
                },
            )
        )

        result = await registry.invoke(
            ToolCall(
                id="c1",
                name="vibemarketolog.generate_image",
                arguments={"prompt": "a house"},
            ),
            ctx,
        )

        assert result.status is ToolStatus.OK

    @respx.mock
    async def test_a_file_means_finished_whatever_the_status_says(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        """Belt and braces: never poll again over an unknown word for 'ready'."""
        respx.post(f"{BASE}/generate").mock(return_value=httpx.Response(200, json={"id": "g"}))
        respx.get(f"{BASE}/generation/g/status").mock(
            return_value=httpx.Response(
                200, json={"status": "finalising", "result_urls": ["https://x/y.png"]}
            )
        )

        result = await registry.invoke(
            ToolCall(
                id="c1",
                name="vibemarketolog.generate_image",
                arguments={"prompt": "a house"},
            ),
            ctx,
        )

        assert result.status is ToolStatus.OK
        assert isinstance(result.data, dict)
        assert result.data["url"] == "https://x/y.png"
