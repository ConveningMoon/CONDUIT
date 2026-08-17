"""The chain: an edit cannot be hidden, only found."""

from __future__ import annotations

import dataclasses
import itertools

import pytest

from conduit.core.agent import Agent, AuditPhase, Plan, PlanRequest
from conduit.core.audit import (
    GENESIS_HASH,
    AuditRecord,
    HashChainAuditSink,
    InMemoryAuditStore,
    verify,
)
from conduit.core.guard import DeterministicGuard, GuardSettings, InMemoryGuardStore
from conduit.core.tools import SideEffect, ToolCall, ToolContext, ToolStatus


def event(**overrides):
    from conduit.core.agent import AuditEvent

    base = {
        "phase": AuditPhase.INTENT,
        "tenant_id": "tenant-conduit-demo",
        "session_id": "telegram:1",
        "actor_id": "telegram:2",
        "request_id": "req-1",
        "call_id": "c1",
        "tool_name": "itmano_crm.list_leads",
        "side_effect": SideEffect.READ,
        "arguments": {"stage": "nuevo"},
    }
    return AuditEvent(**{**base, **overrides})


@pytest.fixture
def sink() -> HashChainAuditSink:
    return HashChainAuditSink(store=InMemoryAuditStore())


async def records(sink: HashChainAuditSink) -> list[AuditRecord]:
    return await sink.store.all()


class TestChaining:
    async def test_the_first_record_links_to_genesis(self, sink: HashChainAuditSink) -> None:
        await sink.record(event())

        first = (await records(sink))[0]
        assert first.sequence == 1
        assert first.previous_hash == GENESIS_HASH

    async def test_each_record_links_to_the_one_before(self, sink: HashChainAuditSink) -> None:
        for n in range(4):
            await sink.record(event(call_id=f"c{n}"))

        chain = await records(sink)
        assert [r.sequence for r in chain] == [1, 2, 3, 4]
        for earlier, later in itertools.pairwise(chain):
            assert later.previous_hash == earlier.entry_hash

    async def test_an_untouched_chain_verifies(self, sink: HashChainAuditSink) -> None:
        for n in range(5):
            await sink.record(event(call_id=f"c{n}"))

        assert verify(await records(sink)) is None

    async def test_identical_events_still_get_distinct_hashes(
        self, sink: HashChainAuditSink
    ) -> None:
        """Sequence and predecessor are part of the digest, so repeats differ."""
        await sink.record(event())
        await sink.record(event())

        chain = await records(sink)
        assert chain[0].entry_hash != chain[1].entry_hash


class TestTampering:
    async def test_editing_a_record_is_detected(self, sink: HashChainAuditSink) -> None:
        for n in range(4):
            await sink.record(event(call_id=f"c{n}"))
        chain = await records(sink)

        # Someone rewrites history: the write was against a different tenant.
        chain[1] = dataclasses.replace(chain[1], event=event(tenant_id="tenant-not-ours"))

        break_ = verify(chain)
        assert break_ is not None
        assert break_.sequence == 2
        assert "stored hash" in break_.problem

    async def test_removing_a_record_is_detected(self, sink: HashChainAuditSink) -> None:
        for n in range(4):
            await sink.record(event(call_id=f"c{n}"))
        chain = await records(sink)

        del chain[1]

        break_ = verify(chain)
        assert break_ is not None
        assert break_.sequence == 3

    async def test_reordering_is_detected(self, sink: HashChainAuditSink) -> None:
        for n in range(4):
            await sink.record(event(call_id=f"c{n}"))
        chain = await records(sink)

        chain[1], chain[2] = chain[2], chain[1]

        assert verify(chain) is not None

    async def test_a_forged_record_appended_to_the_end_is_detected(
        self, sink: HashChainAuditSink
    ) -> None:
        """Appending needs the previous hash, which needs the whole chain."""
        await sink.record(event())
        chain = await records(sink)

        chain.append(
            AuditRecord(
                sequence=2,
                recorded_at=chain[0].recorded_at,
                previous_hash="deadbeef" * 8,
                entry_hash="cafe" * 16,
                event=event(tool_name="itmano_crm.create_lead"),
            )
        )

        break_ = verify(chain)
        assert break_ is not None
        assert break_.sequence == 2

    async def test_an_empty_chain_is_vacuously_fine(self) -> None:
        assert verify([]) is None


class TestThroughTheLoop:
    async def test_intent_is_chained_before_its_outcome(self, registry, ctx: ToolContext) -> None:
        sink = HashChainAuditSink(store=InMemoryAuditStore())

        class Once:
            async def plan(self, request: PlanRequest) -> Plan:
                if request.iteration == 1:
                    return Plan(
                        tool_calls=(ToolCall(id="c1", name="demo.echo", arguments={"text": "hi"}),)
                    )
                return Plan(reply="done")

        agent = Agent(
            registry=registry,
            planner=Once(),
            guard=DeterministicGuard(settings=GuardSettings(), store=InMemoryGuardStore()),
            audit=sink,
        )

        await agent.run("go", ctx)

        chain = await records(sink)
        assert [r.event.phase for r in chain] == [AuditPhase.INTENT, AuditPhase.OUTCOME]
        assert chain[0].event.status is None
        assert chain[1].event.status is ToolStatus.OK
        assert verify(chain) is None

    async def test_a_denied_write_is_in_the_chain_too(self, registry, ctx: ToolContext) -> None:
        """What was refused matters as much as what ran."""
        sink = HashChainAuditSink(store=InMemoryAuditStore())

        class Writes:
            async def plan(self, request: PlanRequest) -> Plan:
                if request.iteration == 1:
                    return Plan(tool_calls=(ToolCall(id="c1", name="demo.write_thing"),))
                return Plan(reply="refused")

        agent = Agent(
            registry=registry,
            planner=Writes(),
            guard=DeterministicGuard(settings=GuardSettings(), store=InMemoryGuardStore()),
            audit=sink,
        )

        await agent.run("write it", ctx)

        chain = await records(sink)
        assert len(chain) == 2
        assert chain[0].event.allowed is False
        assert chain[0].event.guard_rule == "writes_disabled"
        assert chain[1].event.status is ToolStatus.REJECTED
        assert verify(chain) is None
