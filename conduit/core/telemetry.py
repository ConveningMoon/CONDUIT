"""Per-turn ledger of model calls.

Cost and model choice are decisions this system makes on the user's behalf, so
they have to be inspectable. Hiding them in a config file means nobody can check
whether the cheap model was the right call.

Scoped with a context variable rather than an attribute on the planner, because
one planner instance serves every concurrent conversation and an attribute would
mix their ledgers together.
"""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass

__all__ = ["ModelCall", "current_ledger", "record_model_call", "turn_ledger"]


@dataclass(frozen=True, slots=True)
class ModelCall:
    """One billable request made on the user's behalf, and what it cost.

    Not only text. An image generation is the most expensive thing a turn can
    do — seven roubles against one for a planning pass — so leaving it out made
    ``/debug`` report a fraction of the real bill while claiming to be the
    total. Token fields are simply zero for generations, which have none.
    """

    model: str
    cost_rub: float
    latency_ms: int
    input_tokens: int = 0
    output_tokens: int = 0
    cached_tokens: int = 0
    """Prompt tokens served from the provider's cache.

    Worth carrying separately rather than folding into ``input_tokens``: the
    platform bills cache reads at a tenth of the input rate, and a tool
    catalogue is identical on every call, so this is where most of a planning
    prompt ends up. Without it the input count looks impossibly small — three
    tokens for a prompt that is plainly longer than three tokens."""

    retry: bool = False
    """True when this call only happened because the previous one came back
    unparseable. Counted separately: it is waste, and waste worth seeing."""


_LEDGER: ContextVar[list[ModelCall] | None] = ContextVar("conduit_turn_ledger", default=None)


@contextmanager
def turn_ledger() -> Iterator[list[ModelCall]]:
    """Collect every model call made inside this block."""
    entries: list[ModelCall] = []
    token = _LEDGER.set(entries)
    try:
        yield entries
    finally:
        _LEDGER.reset(token)


def record_model_call(call: ModelCall) -> None:
    """Add to the ledger if one is open. A no-op otherwise, never an error."""
    entries = _LEDGER.get()
    if entries is not None:
        entries.append(call)


def current_ledger() -> list[ModelCall]:
    return list(_LEDGER.get() or [])
