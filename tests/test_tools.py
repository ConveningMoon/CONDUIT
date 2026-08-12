"""The calling protocol: validation, isolation of failures, and the freeze."""

from __future__ import annotations

import asyncio

import pytest
from pydantic import BaseModel, ValidationError

from conduit.core.tools import (
    DuplicateToolError,
    RegistryFrozenError,
    SideEffect,
    ToolCall,
    ToolContext,
    ToolErrorCode,
    ToolRegistry,
    ToolResult,
    ToolSpec,
    ToolStatus,
    UnknownToolError,
)
from tests.conftest import EchoParams, NoParams


def _spec(name: str, side_effect: SideEffect = SideEffect.READ) -> ToolSpec:
    return ToolSpec(
        name=name,
        description="A tool.",
        params=NoParams,
        side_effect=side_effect,
    )


class TestSpec:
    def test_name_must_be_namespaced(self) -> None:
        with pytest.raises(ValidationError):
            _spec("echo")

    def test_namespace_is_the_adapter(self) -> None:
        assert _spec("itmano_crm.list_leads").namespace == "itmano_crm"

    def test_json_schema_carries_arguments(self) -> None:
        schema = ToolSpec(
            name="demo.echo",
            description="Repeat the given text.",
            params=EchoParams,
            side_effect=SideEffect.READ,
        ).json_schema()

        assert schema["name"] == "demo.echo"
        assert "text" in schema["parameters"]["properties"]


class TestRegistry:
    def test_registers_and_lists_sorted(self, registry: ToolRegistry) -> None:
        assert [spec.name for spec in registry.specs()] == ["demo.echo", "demo.write_thing"]
        assert "demo.echo" in registry
        assert len(registry) == 2

    def test_filters_by_namespace(self, registry: ToolRegistry) -> None:
        assert registry.specs(namespace="itmano_crm") == []
        assert len(registry.specs(namespace="demo")) == 2

    def test_duplicate_name_is_refused(self, registry: ToolRegistry) -> None:
        async def handler(ctx: ToolContext, params: NoParams) -> ToolResult:
            return ToolResult.ok()

        with pytest.raises(DuplicateToolError):
            registry.register(_spec("demo.echo"), handler)

    def test_unknown_spec_lookup_raises(self, registry: ToolRegistry) -> None:
        with pytest.raises(UnknownToolError):
            registry.spec("demo.nope")

    def test_freeze_blocks_late_registration(self, registry: ToolRegistry) -> None:
        async def handler(ctx: ToolContext, params: NoParams) -> ToolResult:
            return ToolResult.ok()

        registry.freeze()
        assert registry.frozen
        with pytest.raises(RegistryFrozenError):
            registry.register(_spec("demo.late"), handler)


class TestInvoke:
    async def test_happy_path(self, registry: ToolRegistry, ctx: ToolContext) -> None:
        result = await registry.invoke(
            ToolCall(id="c1", name="demo.echo", arguments={"text": "hi", "times": 2}),
            ctx,
        )

        assert result.status is ToolStatus.OK
        assert result.succeeded
        assert result.data == "hi hi"
        assert result.duration_ms >= 0

    async def test_unknown_tool_is_a_result_not_an_exception(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        result = await registry.invoke(ToolCall(id="c1", name="demo.nope"), ctx)

        assert result.status is ToolStatus.FAILED
        assert result.error is not None
        assert result.error.code is ToolErrorCode.NOT_FOUND

    async def test_bad_arguments_never_reach_the_handler(
        self, registry: ToolRegistry, ctx: ToolContext
    ) -> None:
        result = await registry.invoke(
            ToolCall(id="c1", name="demo.echo", arguments={"times": 2}),
            ctx,
        )

        assert result.error is not None
        assert result.error.code is ToolErrorCode.INVALID_ARGUMENTS

    async def test_a_raising_handler_becomes_an_internal_error(self, ctx: ToolContext) -> None:
        reg = ToolRegistry()

        @reg.tool(
            name="demo.boom",
            description="Always explodes.",
            params=NoParams,
            side_effect=SideEffect.READ,
        )
        async def boom(ctx: ToolContext, params: NoParams) -> ToolResult:
            raise RuntimeError("upstream is on fire")

        result = await reg.invoke(ToolCall(id="c1", name="demo.boom"), ctx)

        assert result.error is not None
        assert result.error.code is ToolErrorCode.INTERNAL
        assert "upstream is on fire" in result.error.message

    async def test_a_slow_handler_times_out(self, ctx: ToolContext) -> None:
        reg = ToolRegistry()

        @reg.tool(
            name="demo.slow",
            description="Never finishes in time.",
            params=NoParams,
            side_effect=SideEffect.READ,
            timeout_seconds=0.01,
        )
        async def slow(ctx: ToolContext, params: NoParams) -> ToolResult:
            await asyncio.sleep(1)
            return ToolResult.ok()

        result = await reg.invoke(ToolCall(id="c1", name="demo.slow"), ctx)

        assert result.error is not None
        assert result.error.code is ToolErrorCode.TIMEOUT
        assert result.error.retryable

    async def test_context_reaches_the_handler(self, ctx: ToolContext) -> None:
        reg = ToolRegistry()
        seen: list[str] = []

        @reg.tool(
            name="demo.whoami",
            description="Reports the tenant it was called for.",
            params=NoParams,
            side_effect=SideEffect.READ,
        )
        async def whoami(ctx: ToolContext, params: NoParams) -> ToolResult:
            seen.append(ctx.tenant_id)
            return ToolResult.ok(ctx.tenant_id)

        await reg.invoke(ToolCall(id="c1", name="demo.whoami"), ctx)

        assert seen == ["tenant-demo"]


class TestResultEnvelope:
    def test_results_are_json_serialisable(self) -> None:
        payload = ToolResult.failed(ToolErrorCode.UPSTREAM_ERROR, "502").model_dump_json()

        assert '"upstream_error"' in payload

    def test_results_are_immutable(self) -> None:
        result = ToolResult.ok(1)

        with pytest.raises(ValidationError):
            result.status = ToolStatus.FAILED  # type: ignore[misc]

    def test_data_must_be_json(self) -> None:
        class NotJson(BaseModel):
            pass

        with pytest.raises(ValidationError):
            ToolResult.ok(NotJson())  # type: ignore[arg-type]
