"""Deterministic limits in front of every action.

Seven rules, checked in a fixed order, cheapest and most decisive first. Not one
of them consults a model: an LLM on the critical path before an action costs
money and latency to answer a question that arithmetic already answers. A model
belongs here only for genuine ambiguity left over *after* all of these pass, and
nothing in this module does that yet.

The order is not cosmetic. The kill switch runs first because when someone pulls
it they want everything to stop, including things that would otherwise be fine.
Loop detection runs last because it is the only rule that has to write state.
"""

from __future__ import annotations

import hashlib
import json
import time
from collections import deque
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from conduit.core.agent import GuardDecision
from conduit.core.tools import SideEffect, ToolCall, ToolContext, ToolSpec

__all__ = [
    "DeterministicGuard",
    "GuardRule",
    "GuardSettings",
    "GuardStore",
    "InMemoryGuardStore",
    "intent_hash",
]


class GuardRule(StrEnum):
    """Which rule decided. Recorded on every decision, allow or deny."""

    KILL_SWITCH = "kill_switch"
    NOT_WHITELISTED = "not_whitelisted"
    WRITES_DISABLED = "writes_disabled"
    NEEDS_CONFIRMATION = "needs_confirmation"
    TURN_CALL_CEILING = "turn_call_ceiling"
    ACTION_CEILING = "action_ceiling"
    LOOP_DETECTED = "loop_detected"
    WRITE_ALREADY_ATTEMPTED = "write_already_attempted"
    PASSED = "passed"


class GuardSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GUARD_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    max_tool_calls_per_turn: int = Field(default=8, ge=1)
    max_actions_per_session_hour: int = Field(default=40, ge=0)
    loop_window_seconds: float = Field(default=300.0, gt=0)
    loop_repeat_threshold: int = Field(default=3, ge=2)

    allow_writes: bool = False
    """Default closed. A deployment that has not said yes cannot mutate anything."""

    whitelist: frozenset[str] = frozenset()
    """Empty means every registered tool is eligible, subject to the other rules.
    A non-empty set is exhaustive: anything outside it is denied."""


def intent_hash(call: ToolCall) -> str:
    """A stable fingerprint of *what is being attempted*.

    Arguments are canonicalised — sorted keys, no whitespace — so that the same
    intent expressed with keys in a different order collapses to one hash. Loop
    detection is worthless otherwise: a planner stuck in a circle rarely emits
    byte-identical JSON.
    """
    canonical = json.dumps(call.arguments, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(f"{call.name}\n{canonical}".encode()).hexdigest()[:32]


class GuardStore(Protocol):
    """Counters and switches the rules read and write.

    Deliberately narrow, and every method is async, so that a Redis-backed
    implementation is a drop-in: kill switch as a key, the windows as sorted
    sets with expiry.
    """

    async def is_stopped(self, tenant_id: str) -> bool: ...

    async def note_call(self, request_id: str) -> int:
        """Record a call in this turn and return the running count, this one included."""
        ...

    async def note_action(self, session_id: str, now: float) -> int:
        """Record a write and return how many happened in the trailing hour."""
        ...

    async def note_intent(self, session_id: str, fingerprint: str, now: float) -> int:
        """Record an intent and return how often it occurred inside the window."""
        ...


@dataclass(slots=True)
class InMemoryGuardStore:
    """Process-local implementation. Correct, and forgets everything on restart.

    Good enough for a single process; the moment there are two, the ceilings stop
    being ceilings and this needs Redis behind the same Protocol.
    """

    loop_window_seconds: float = 300.0
    action_window_seconds: float = 3600.0

    stopped_tenants: set[str] = field(default_factory=set)
    _calls: dict[str, int] = field(default_factory=dict)
    _actions: dict[str, deque[float]] = field(default_factory=dict)
    _intents: dict[tuple[str, str], deque[float]] = field(default_factory=dict)

    def stop(self, tenant_id: str) -> None:
        """Engage the kill switch. Synchronous on purpose: an operator action."""
        self.stopped_tenants.add(tenant_id)

    def resume(self, tenant_id: str) -> None:
        self.stopped_tenants.discard(tenant_id)

    async def is_stopped(self, tenant_id: str) -> bool:
        return tenant_id in self.stopped_tenants

    async def note_call(self, request_id: str) -> int:
        self._calls[request_id] = self._calls.get(request_id, 0) + 1
        return self._calls[request_id]

    async def note_action(self, session_id: str, now: float) -> int:
        window = self._actions.setdefault(session_id, deque())
        window.append(now)
        self._evict(window, now - self.action_window_seconds)
        return len(window)

    async def note_intent(self, session_id: str, fingerprint: str, now: float) -> int:
        window = self._intents.setdefault((session_id, fingerprint), deque())
        window.append(now)
        self._evict(window, now - self.loop_window_seconds)
        return len(window)

    @staticmethod
    def _evict(window: deque[float], cutoff: float) -> None:
        while window and window[0] < cutoff:
            window.popleft()


@dataclass(slots=True)
class DeterministicGuard:
    """The guard the orchestration loop consults before every call."""

    settings: GuardSettings = field(default_factory=GuardSettings)
    store: GuardStore = field(default_factory=InMemoryGuardStore)
    confirmed: frozenset[str] = frozenset()
    """Intent hashes a human has approved this session. Phase 4 has no channel
    for collecting them; the seam exists so that adding one changes nothing else."""

    async def review(self, call: ToolCall, spec: ToolSpec, ctx: ToolContext) -> GuardDecision:
        if await self.store.is_stopped(ctx.tenant_id):
            return GuardDecision.deny(
                "the kill switch is engaged for this tenant",
                rule=GuardRule.KILL_SWITCH,
            )

        if self.settings.whitelist and call.name not in self.settings.whitelist:
            return GuardDecision.deny(
                f"{call.name} is not on the whitelist",
                rule=GuardRule.NOT_WHITELISTED,
            )

        is_write = spec.side_effect is SideEffect.WRITE
        if is_write and not self.settings.allow_writes:
            return GuardDecision.deny(
                "writes are disabled in this deployment",
                rule=GuardRule.WRITES_DISABLED,
            )

        fingerprint = intent_hash(call)
        if spec.requires_confirmation and fingerprint not in self.confirmed:
            return GuardDecision.deny(
                f"{call.name} needs a human to confirm it first",
                rule=GuardRule.NEEDS_CONFIRMATION,
            )

        calls_this_turn = await self.store.note_call(ctx.request_id)
        if calls_this_turn > self.settings.max_tool_calls_per_turn:
            return GuardDecision.deny(
                f"this turn already made {self.settings.max_tool_calls_per_turn} calls",
                rule=GuardRule.TURN_CALL_CEILING,
            )

        now = time.monotonic()

        if is_write:
            actions = await self.store.note_action(ctx.session_id, now)
            if actions > self.settings.max_actions_per_session_hour:
                return GuardDecision.deny(
                    f"this session already made "
                    f"{self.settings.max_actions_per_session_hour} changes this hour",
                    rule=GuardRule.ACTION_CEILING,
                )

        if is_write:
            # A write that already ran once in this turn does not get a second
            # go without a human asking for it. The general loop rule allows two
            # repeats before tripping, which is right for a read and wrong for
            # anything irreversible: a failed image generation is refunded, but
            # a retried one that succeeds twice is paid for twice. Observed in a
            # rehearsal, where a transient platform error made the planner
            # cheerfully try again on its own.
            attempts = await self.store.note_intent(ctx.request_id, fingerprint, now)
            if attempts > 1:
                return GuardDecision.deny(
                    "this exact change was already attempted in this turn; "
                    "ask again if you want it retried",
                    rule=GuardRule.WRITE_ALREADY_ATTEMPTED,
                )

        repeats = await self.store.note_intent(ctx.session_id, fingerprint, now)
        if repeats >= self.settings.loop_repeat_threshold:
            return GuardDecision.deny(
                f"the same call was attempted {repeats} times in "
                f"{self.settings.loop_window_seconds:g}s",
                rule=GuardRule.LOOP_DETECTED,
            )

        return GuardDecision.allow(rule=GuardRule.PASSED)
