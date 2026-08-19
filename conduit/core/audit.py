"""Tamper-evident action log.

Each record carries the hash of the one before it, so the log is a chain rather
than a pile. Altering or removing a record breaks every hash after it, and
:func:`verify` finds the first break. That is the whole property: not that the
log cannot be edited, but that an edit cannot be hidden.

The agent writes twice per call — the intent before it runs, the outcome after.
Both go in the chain. If the process dies between them, the log still says what
was about to happen, which is the question anyone actually asks afterwards.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Protocol

from conduit.core.agent import AuditEvent

__all__ = [
    "GENESIS_HASH",
    "AuditRecord",
    "AuditStore",
    "ChainBreak",
    "HashChainAuditSink",
    "InMemoryAuditStore",
    "verify",
]

GENESIS_HASH = "0" * 64
"""What the first record links to. A chain has to start somewhere, and an
explicit constant beats a nullable column that invites a special case."""


@dataclass(frozen=True, slots=True)
class AuditRecord:
    """One link. Immutable by construction; the store only ever appends."""

    sequence: int
    recorded_at: datetime
    previous_hash: str
    entry_hash: str
    event: AuditEvent

    def compute_hash(self) -> str:
        """Recompute this record's hash from its contents.

        Uses pydantic's canonical JSON for the event, so field order cannot
        change the digest between runs.
        """
        payload = "\n".join(
            [
                str(self.sequence),
                self.recorded_at.isoformat(),
                self.previous_hash,
                self.event.model_dump_json(),
            ]
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


class AuditStore(Protocol):
    """Append-only storage. No update, no delete — not as policy, as API."""

    async def append(self, record: AuditRecord) -> None: ...

    async def last(self) -> AuditRecord | None: ...

    async def all(self) -> list[AuditRecord]: ...


@dataclass(slots=True)
class InMemoryAuditStore:
    """Process-local chain. Replaced by Postgres, behind the same Protocol."""

    records: list[AuditRecord] = field(default_factory=list)

    async def append(self, record: AuditRecord) -> None:
        self.records.append(record)

    async def last(self) -> AuditRecord | None:
        return self.records[-1] if self.records else None

    async def all(self) -> list[AuditRecord]:
        return list(self.records)


@dataclass(slots=True)
class HashChainAuditSink:
    """An :class:`~conduit.core.agent.AuditSink` that chains what it records."""

    store: AuditStore = field(default_factory=InMemoryAuditStore)

    async def record(self, event: AuditEvent) -> None:
        previous = await self.store.last()
        sequence = previous.sequence + 1 if previous else 1
        previous_hash = previous.entry_hash if previous else GENESIS_HASH

        draft = AuditRecord(
            sequence=sequence,
            recorded_at=datetime.now(UTC),
            previous_hash=previous_hash,
            entry_hash="",
            event=event,
        )
        sealed = AuditRecord(
            sequence=draft.sequence,
            recorded_at=draft.recorded_at,
            previous_hash=draft.previous_hash,
            entry_hash=draft.compute_hash(),
            event=draft.event,
        )
        await self.store.append(sealed)


@dataclass(frozen=True, slots=True)
class ChainBreak:
    """Where the chain stops adding up, and why."""

    sequence: int
    problem: str


def verify(records: list[AuditRecord]) -> ChainBreak | None:
    """Walk the chain. Returns the first break, or ``None`` if it holds.

    Three ways it can fail, and each is a different story: a record whose own
    hash does not match its contents was edited; a record whose link does not
    match its predecessor means something was removed or reordered; a gap in the
    sequence means a record is missing outright.
    """
    expected_hash = GENESIS_HASH
    expected_sequence = 1

    for record in records:
        if record.sequence != expected_sequence:
            return ChainBreak(
                sequence=record.sequence,
                problem=f"expected sequence {expected_sequence}, found {record.sequence}",
            )
        if record.previous_hash != expected_hash:
            return ChainBreak(
                sequence=record.sequence,
                problem="previous_hash does not match the record before it",
            )
        if record.compute_hash() != record.entry_hash:
            return ChainBreak(
                sequence=record.sequence,
                problem="contents do not match the stored hash",
            )
        expected_hash = record.entry_hash
        expected_sequence += 1

    return None
