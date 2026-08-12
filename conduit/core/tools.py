"""Tool registry and calling protocol.

This module is the contract every other part of CONDUIT consumes: adapters
publish tools into a :class:`ToolRegistry`, the guard inspects the declared
:class:`ToolSpec` before anything runs, the audit log serialises the
:class:`ToolCall` and :class:`ToolResult` pair, and the planner sees only the
JSON schemas.

Nothing here knows what a lead or a deal is. A tool is a name, a typed argument
model, a declared side effect and an async handler.
"""

from __future__ import annotations

import asyncio
import time
from collections.abc import Awaitable, Callable, Iterator, Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Protocol, cast

from pydantic import BaseModel, ConfigDict, Field, JsonValue, ValidationError

__all__ = [
    "AnyToolHandler",
    "DuplicateToolError",
    "RegistryFrozenError",
    "SideEffect",
    "ToolCall",
    "ToolContext",
    "ToolError",
    "ToolErrorCode",
    "ToolHandler",
    "ToolRegistry",
    "ToolResult",
    "ToolSpec",
    "ToolStatus",
    "UnknownToolError",
]

DEFAULT_TIMEOUT_SECONDS = 20.0


class SideEffect(StrEnum):
    """What a tool does to the world.

    The guard treats these very differently: ``READ`` is cheap to allow, ``WRITE``
    is what ceilings, whitelists and the audit chain exist for.
    """

    READ = "read"
    WRITE = "write"


class ToolStatus(StrEnum):
    """Outcome of an invocation, from the caller's point of view."""

    OK = "ok"
    FAILED = "failed"
    REJECTED = "rejected"


class ToolErrorCode(StrEnum):
    """Provider-agnostic failure taxonomy.

    Adapters map their own upstream errors onto these so the planner sees one
    vocabulary regardless of which business system answered.
    """

    INVALID_ARGUMENTS = "invalid_arguments"
    NOT_FOUND = "not_found"
    UNAUTHORIZED = "unauthorized"
    RATE_LIMITED = "rate_limited"
    UPSTREAM_ERROR = "upstream_error"
    TIMEOUT = "timeout"
    REJECTED_BY_GUARD = "rejected_by_guard"
    INTERNAL = "internal"


class ToolError(BaseModel):
    """Structured failure detail. Safe to serialise into the audit log."""

    model_config = ConfigDict(frozen=True)

    code: ToolErrorCode
    message: str
    retryable: bool = False


class ToolResult(BaseModel):
    """Uniform envelope returned by every tool.

    Handlers return this instead of raising, so a failing adapter degrades into
    a fact the planner can reason about rather than an exception that kills the
    turn. The registry converts any escaped exception into one of these anyway.
    """

    model_config = ConfigDict(frozen=True)

    status: ToolStatus
    data: JsonValue = None
    error: ToolError | None = None
    duration_ms: int = 0

    @classmethod
    def ok(cls, data: JsonValue = None) -> ToolResult:
        return cls(status=ToolStatus.OK, data=data)

    @classmethod
    def failed(
        cls,
        code: ToolErrorCode,
        message: str,
        *,
        retryable: bool = False,
    ) -> ToolResult:
        return cls(
            status=ToolStatus.FAILED,
            error=ToolError(code=code, message=message, retryable=retryable),
        )

    @classmethod
    def rejected(cls, message: str) -> ToolResult:
        return cls(
            status=ToolStatus.REJECTED,
            error=ToolError(code=ToolErrorCode.REJECTED_BY_GUARD, message=message),
        )

    @property
    def succeeded(self) -> bool:
        return self.status is ToolStatus.OK


class ToolCall(BaseModel):
    """A request to run one tool, as the planner emits it."""

    model_config = ConfigDict(frozen=True)

    id: str
    name: str
    arguments: dict[str, JsonValue] = Field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class ToolContext:
    """Per-invocation identity and correlation.

    ``tenant_id`` is carried, never enforced here. Tenant isolation is the CRM's
    job; CONDUIT only presents the identity it was given and receives whatever
    that tenant is allowed to see.
    """

    tenant_id: str
    session_id: str
    actor_id: str
    request_id: str
    idempotency_key: str | None = None
    locale: str = "en"
    extras: Mapping[str, str] = field(default_factory=dict)


class ToolHandler[P: BaseModel](Protocol):
    """The shape of a tool implementation."""

    async def __call__(self, ctx: ToolContext, params: P) -> ToolResult: ...


AnyToolHandler = Callable[[ToolContext, Any], Awaitable[ToolResult]]


class ToolSpec(BaseModel):
    """Everything the rest of the system needs to know about a tool.

    Declared once by the adapter, then consumed by the planner (schema), the
    guard (``side_effect``, ``requires_confirmation``) and the cost ledger
    (``estimated_cost_usd``).
    """

    model_config = ConfigDict(frozen=True)

    name: str = Field(pattern=r"^[a-z][a-z0-9_]*\.[a-z][a-z0-9_]*$")
    description: str = Field(min_length=1)
    params: type[BaseModel]
    side_effect: SideEffect
    requires_confirmation: bool = False
    estimated_cost_usd: float = Field(default=0.0, ge=0.0)
    timeout_seconds: float = Field(default=DEFAULT_TIMEOUT_SECONDS, gt=0.0)

    @property
    def namespace(self) -> str:
        """Adapter this tool belongs to, e.g. ``itmano_crm``."""
        return self.name.split(".", 1)[0]

    def json_schema(self) -> dict[str, Any]:
        """Argument schema, in the form a function-calling planner expects."""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.params.model_json_schema(),
        }


class DuplicateToolError(ValueError):
    """Raised when two tools claim the same name."""


class UnknownToolError(KeyError):
    """Raised when a name is looked up that was never registered."""


class RegistryFrozenError(RuntimeError):
    """Raised on an attempt to register after the registry was frozen."""


@dataclass(frozen=True, slots=True)
class RegisteredTool:
    spec: ToolSpec
    handler: AnyToolHandler


class ToolRegistry:
    """Name-to-implementation map, populated at startup and then frozen.

    Freezing matters: the set of tools a session can reach must not change while
    that session is mid-turn, or the guard's whitelist stops meaning anything.
    """

    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}
        self._frozen = False

    def __contains__(self, name: object) -> bool:
        return name in self._tools

    def __len__(self) -> int:
        return len(self._tools)

    def __iter__(self) -> Iterator[ToolSpec]:
        return iter(self.specs())

    @property
    def frozen(self) -> bool:
        return self._frozen

    def freeze(self) -> None:
        self._frozen = True

    def register[P: BaseModel](self, spec: ToolSpec, handler: ToolHandler[P]) -> None:
        """Add a tool. Raises rather than silently replacing an existing name."""
        if self._frozen:
            raise RegistryFrozenError(f"cannot register {spec.name!r}: registry is frozen")
        if spec.name in self._tools:
            raise DuplicateToolError(f"tool {spec.name!r} is already registered")
        self._tools[spec.name] = RegisteredTool(
            spec=spec,
            handler=cast(AnyToolHandler, handler),
        )

    def tool[P: BaseModel](
        self,
        *,
        name: str,
        description: str,
        params: type[P],
        side_effect: SideEffect,
        requires_confirmation: bool = False,
        estimated_cost_usd: float = 0.0,
        timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS,
    ) -> Callable[[ToolHandler[P]], ToolHandler[P]]:
        """Decorator form of :meth:`register`."""

        def decorate(handler: ToolHandler[P]) -> ToolHandler[P]:
            self.register(
                ToolSpec(
                    name=name,
                    description=description,
                    params=params,
                    side_effect=side_effect,
                    requires_confirmation=requires_confirmation,
                    estimated_cost_usd=estimated_cost_usd,
                    timeout_seconds=timeout_seconds,
                ),
                handler,
            )
            return handler

        return decorate

    def spec(self, name: str) -> ToolSpec:
        try:
            return self._tools[name].spec
        except KeyError:
            raise UnknownToolError(name) from None

    def specs(self, *, namespace: str | None = None) -> list[ToolSpec]:
        """Every spec, or only those of one adapter, sorted by name."""
        specs = [entry.spec for entry in self._tools.values()]
        if namespace is not None:
            specs = [spec for spec in specs if spec.namespace == namespace]
        return sorted(specs, key=lambda spec: spec.name)

    def json_schemas(self, *, namespace: str | None = None) -> list[dict[str, Any]]:
        """What the planner is shown."""
        return [spec.json_schema() for spec in self.specs(namespace=namespace)]

    async def invoke(self, call: ToolCall, ctx: ToolContext) -> ToolResult:
        """Validate, run and time one call. Never raises.

        Anything a handler throws becomes an ``INTERNAL`` result, because the
        orchestration loop has to stay alive long enough to tell the user what
        went wrong.
        """
        entry = self._tools.get(call.name)
        if entry is None:
            return ToolResult.failed(
                ToolErrorCode.NOT_FOUND,
                f"no tool named {call.name!r}",
            )

        try:
            params = entry.spec.params.model_validate(call.arguments)
        except ValidationError as exc:
            return ToolResult.failed(
                ToolErrorCode.INVALID_ARGUMENTS,
                f"arguments rejected by {call.name}: {exc.error_count()} problem(s); {exc}",
            )

        started = time.perf_counter()
        try:
            async with asyncio.timeout(entry.spec.timeout_seconds):
                result = await entry.handler(ctx, params)
        except TimeoutError:
            result = ToolResult.failed(
                ToolErrorCode.TIMEOUT,
                f"{call.name} exceeded {entry.spec.timeout_seconds:g}s",
                retryable=True,
            )
        except asyncio.CancelledError:
            raise
        # Deliberately broad: a misbehaving adapter must not kill the turn.
        except Exception as exc:
            result = ToolResult.failed(
                ToolErrorCode.INTERNAL,
                f"{call.name} raised {type(exc).__name__}: {exc}",
            )

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return result.model_copy(update={"duration_ms": elapsed_ms})
