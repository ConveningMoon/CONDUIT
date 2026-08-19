"""Orchestration loop: intent, plan, guard, execute, report.

The loop owns the ordering guarantees, nothing else. It does not know which
model produced a plan, which business system a tool talks to, or how the guard
reaches a verdict — those arrive as :class:`Planner`, :class:`ToolRegistry` and
:class:`Guard` implementations.

Two invariants hold here and are worth stating plainly:

1. **The guard runs before every call**, including calls the planner is certain
   about. A denied call becomes a ``REJECTED`` result fed back to the planner,
   never an exception.
2. **The intent is audited before the action runs.** If the process dies
   mid-write, the log still shows what was about to happen.
"""

from __future__ import annotations

import contextlib
from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from conduit.core.tools import (
    SideEffect,
    ToolCall,
    ToolContext,
    ToolRegistry,
    ToolResult,
    ToolSpec,
    ToolStatus,
)

__all__ = [
    "Agent",
    "AgentReply",
    "AuditEvent",
    "AuditPhase",
    "AuditSink",
    "ExecutedCall",
    "Guard",
    "GuardDecision",
    "NullAuditSink",
    "Plan",
    "PlanRequest",
    "Planner",
    "ReadOnlyGuard",
    "Role",
    "StepReporter",
    "StopReason",
    "Turn",
]

DEFAULT_MAX_ITERATIONS = 4


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class Turn(BaseModel):
    """One entry in the conversation transcript."""

    model_config = ConfigDict(frozen=True)

    role: Role
    content: str
    tool_call_id: str | None = None
    tool_name: str | None = None


class PlanRequest(BaseModel):
    """What the planner is given. Deliberately model-agnostic."""

    model_config = ConfigDict(frozen=True)

    history: tuple[Turn, ...]
    tools: tuple[ToolSpec, ...]
    iteration: int = 1


class Plan(BaseModel):
    """What the planner returns.

    A plan with no tool calls ends the turn; ``reply`` is then what the user
    reads. A plan with tool calls may also carry a ``reply``, which the
    interface can surface as a progress note while the calls run.
    """

    model_config = ConfigDict(frozen=True)

    reply: str = ""
    tool_calls: tuple[ToolCall, ...] = ()

    @property
    def is_final(self) -> bool:
        return not self.tool_calls


class Planner(Protocol):
    """Turns a transcript plus a tool catalogue into the next step."""

    async def plan(self, request: PlanRequest) -> Plan: ...


class GuardDecision(BaseModel):
    """Verdict on a single proposed call."""

    model_config = ConfigDict(frozen=True)

    allowed: bool
    reason: str = ""
    rule: str = ""

    @classmethod
    def allow(cls, rule: str = "") -> GuardDecision:
        return cls(allowed=True, rule=rule)

    @classmethod
    def deny(cls, reason: str, rule: str = "") -> GuardDecision:
        return cls(allowed=False, reason=reason, rule=rule)


class Guard(Protocol):
    """Deterministic-first gate in front of every call.

    Implementations run cheap checks — ceilings, whitelist, loop detection, kill
    switch — before considering anything expensive. See ``conduit.core.guard``.
    """

    async def review(self, call: ToolCall, spec: ToolSpec, ctx: ToolContext) -> GuardDecision: ...


class ReadOnlyGuard:
    """Default guard until ``conduit.core.guard`` lands: reads pass, writes do not.

    Failing closed on writes means an incompletely wired deployment cannot
    mutate a business system by accident.
    """

    async def review(self, call: ToolCall, spec: ToolSpec, ctx: ToolContext) -> GuardDecision:
        if spec.side_effect is SideEffect.WRITE:
            return GuardDecision.deny(
                "write tools are disabled until the guard is wired",
                rule="placeholder_guard",
            )
        return GuardDecision.allow(rule="placeholder_guard")


class AuditPhase(StrEnum):
    """``INTENT`` is written before the call runs, ``OUTCOME`` after."""

    INTENT = "intent"
    OUTCOME = "outcome"


class AuditEvent(BaseModel):
    """One record in the action log. Serialisable, no live objects."""

    model_config = ConfigDict(frozen=True)

    phase: AuditPhase
    tenant_id: str
    session_id: str
    actor_id: str
    request_id: str
    call_id: str
    tool_name: str
    side_effect: SideEffect
    arguments: dict[str, JsonValue] = Field(default_factory=dict)
    allowed: bool | None = None
    guard_reason: str = ""
    guard_rule: str = ""
    status: ToolStatus | None = None
    duration_ms: int | None = None


class AuditSink(Protocol):
    """Where action records go. The hash chain lives in the implementation."""

    async def record(self, event: AuditEvent) -> None: ...


class NullAuditSink:
    """Discards everything. Only acceptable in tests and phase-1 scaffolding."""

    async def record(self, event: AuditEvent) -> None:
        return None


class StepReporter(Protocol):
    """Notified of every call the loop considered, with the guard's verdict.

    The point is not decoration. A turn that takes seconds is a black box unless
    something says what the agent decided; showing the tool and its arguments
    turns a wait into visible reasoning, and makes a wrong choice legible at the
    moment it is made rather than after the answer comes out wrong.

    Refusals are reported too, and deliberately: the guard stopping something is
    the most interesting thing a turn can contain, and it would otherwise surface
    only in the final answer, once the moment has passed.
    """

    async def __call__(self, call: ToolCall, spec: ToolSpec, decision: GuardDecision) -> None: ...


class StopReason(StrEnum):
    COMPLETED = "completed"
    MAX_ITERATIONS = "max_iterations"
    PLANNER_FAILED = "planner_failed"


class ExecutedCall(BaseModel):
    """A call the loop actually considered, and what came of it."""

    model_config = ConfigDict(frozen=True)

    call: ToolCall
    decision: GuardDecision
    result: ToolResult


class AgentReply(BaseModel):
    """The outcome of one user turn."""

    model_config = ConfigDict(frozen=True)

    text: str
    stop_reason: StopReason
    error: str = ""
    transcript: tuple[Turn, ...] = ()
    calls: tuple[ExecutedCall, ...] = ()

    @property
    def iterations(self) -> int:
        return sum(1 for turn in self.transcript if turn.role is Role.ASSISTANT)


@dataclass(slots=True)
class Agent:
    """Runs one user turn to completion.

    ``max_iterations`` bounds plan/execute cycles. It is a hard stop, not a
    guard rule: the guard limits what may happen, this limits how long we keep
    asking.
    """

    registry: ToolRegistry
    planner: Planner
    guard: Guard = field(default_factory=ReadOnlyGuard)
    audit: AuditSink = field(default_factory=NullAuditSink)
    on_step: StepReporter | None = None
    max_iterations: int = DEFAULT_MAX_ITERATIONS

    async def run(
        self,
        message: str,
        ctx: ToolContext,
        history: Sequence[Turn] = (),
    ) -> AgentReply:
        transcript: list[Turn] = [*history, Turn(role=Role.USER, content=message)]
        executed: list[ExecutedCall] = []
        specs = tuple(self.registry.specs())
        last_reply = ""

        for iteration in range(1, self.max_iterations + 1):
            request = PlanRequest(
                history=tuple(transcript),
                tools=specs,
                iteration=iteration,
            )
            try:
                plan = await self.planner.plan(request)
            # Deliberately broad: a planner failure is reported, not raised at
            # the messaging interface.
            except Exception as exc:
                return AgentReply(
                    text=last_reply,
                    stop_reason=StopReason.PLANNER_FAILED,
                    error=f"{type(exc).__name__}: {exc}",
                    transcript=tuple(transcript),
                    calls=tuple(executed),
                )

            if plan.reply:
                last_reply = plan.reply
                transcript.append(Turn(role=Role.ASSISTANT, content=plan.reply))

            if plan.is_final:
                return AgentReply(
                    text=last_reply,
                    stop_reason=StopReason.COMPLETED,
                    transcript=tuple(transcript),
                    calls=tuple(executed),
                )

            for call in plan.tool_calls:
                outcome = await self._execute(call, ctx)
                executed.append(outcome)
                transcript.append(
                    Turn(
                        role=Role.TOOL,
                        content=outcome.result.model_dump_json(),
                        tool_call_id=call.id,
                        tool_name=call.name,
                    )
                )

        return AgentReply(
            text=last_reply,
            stop_reason=StopReason.MAX_ITERATIONS,
            transcript=tuple(transcript),
            calls=tuple(executed),
        )

    async def _execute(self, call: ToolCall, ctx: ToolContext) -> ExecutedCall:
        """Guard, audit the intent, run, audit the outcome. In that order."""
        try:
            spec = self.registry.spec(call.name)
        except KeyError:
            return ExecutedCall(
                call=call,
                decision=GuardDecision.deny("unknown tool", rule="registry"),
                result=ToolResult.rejected(f"no tool named {call.name!r}"),
            )

        decision = await self.guard.review(call, spec, ctx)
        await self.audit.record(self._event(AuditPhase.INTENT, call, spec, ctx, decision=decision))

        if self.on_step is not None:
            # Announced whatever the verdict: a refusal is the most interesting
            # thing that can happen in a turn, and hiding it until the final
            # answer wastes the moment. Reporting must never be able to break
            # the turn it narrates.
            with contextlib.suppress(Exception):
                await self.on_step(call, spec, decision)

        if decision.allowed:
            result = await self.registry.invoke(call, ctx)
        else:
            result = ToolResult.rejected(decision.reason)

        await self.audit.record(
            self._event(AuditPhase.OUTCOME, call, spec, ctx, decision=decision, result=result)
        )
        return ExecutedCall(call=call, decision=decision, result=result)

    @staticmethod
    def _event(
        phase: AuditPhase,
        call: ToolCall,
        spec: ToolSpec,
        ctx: ToolContext,
        *,
        decision: GuardDecision,
        result: ToolResult | None = None,
    ) -> AuditEvent:
        return AuditEvent(
            phase=phase,
            tenant_id=ctx.tenant_id,
            session_id=ctx.session_id,
            actor_id=ctx.actor_id,
            request_id=ctx.request_id,
            call_id=call.id,
            tool_name=call.name,
            side_effect=spec.side_effect,
            arguments=dict(call.arguments),
            allowed=decision.allowed,
            guard_reason=decision.reason,
            guard_rule=decision.rule,
            status=result.status if result is not None else None,
            duration_ms=result.duration_ms if result is not None else None,
        )
