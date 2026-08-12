"""Shared fixtures. Nothing here talks to a real system."""

from __future__ import annotations

import pytest
from pydantic import BaseModel

from conduit.core.tools import SideEffect, ToolContext, ToolRegistry, ToolResult


class EchoParams(BaseModel):
    text: str
    times: int = 1


class NoParams(BaseModel):
    pass


@pytest.fixture
def ctx() -> ToolContext:
    return ToolContext(
        tenant_id="tenant-demo",
        session_id="session-1",
        actor_id="telegram:42",
        request_id="req-1",
    )


@pytest.fixture
def registry() -> ToolRegistry:
    reg = ToolRegistry()

    @reg.tool(
        name="demo.echo",
        description="Repeat the given text.",
        params=EchoParams,
        side_effect=SideEffect.READ,
    )
    async def echo(ctx: ToolContext, params: EchoParams) -> ToolResult:
        return ToolResult.ok(" ".join([params.text] * params.times))

    @reg.tool(
        name="demo.write_thing",
        description="Pretend to write something.",
        params=NoParams,
        side_effect=SideEffect.WRITE,
    )
    async def write_thing(ctx: ToolContext, params: NoParams) -> ToolResult:
        return ToolResult.ok({"written": True})

    return reg
