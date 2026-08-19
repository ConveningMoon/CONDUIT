"""Measure what a CRM tool call actually costs, through the real invocation path.

Runs from CI, not from a laptop: this needs an egress the platform in front of
the CRM does not challenge.

The interesting number is not any single endpoint, it is the decomposition.
``whoami`` reads no business data, so its cost is almost entirely the
authentication chain — token lookup, JWT mint, rate-limit count — that every
other call pays before it starts doing anything useful. The gap between
``whoami`` and a real query is what the query itself costs.
"""

from __future__ import annotations

import asyncio
import statistics
import time
from typing import Any

from conduit.adapters.itmano_crm import ItmanoCrmClient, ItmanoCrmSettings
from conduit.adapters.itmano_crm.tools import register
from conduit.core.tools import ToolCall, ToolContext, ToolRegistry, ToolStatus

REPEATS = 10
"""Kept modest on purpose: the server allows 120 requests/min per token."""

CTX = ToolContext(
    tenant_id="tenant-conduit-demo",
    session_id="measurement",
    actor_id="ci",
    request_id="measure-1",
)

SAMPLES: list[tuple[str, dict[str, Any]]] = [
    ("itmano_crm.whoami", {}),
    ("itmano_crm.metadata", {}),
    ("itmano_crm.list_leads", {"limit": 25}),
    ("itmano_crm.list_deals", {"limit": 25}),
    ("itmano_crm.search", {"q": "Camila", "limit": 10}),
]

TURN = [
    ("itmano_crm.metadata", {}),
    ("itmano_crm.list_leads", {"stage": "en_proceso", "limit": 10}),
]


async def timed(registry: ToolRegistry, name: str, arguments: dict[str, Any]) -> float:
    started = time.perf_counter()
    result = await registry.invoke(ToolCall(id="m", name=name, arguments=arguments), CTX)
    elapsed = (time.perf_counter() - started) * 1000
    if result.status is not ToolStatus.OK:
        raise SystemExit(f"{name} failed during measurement: {result.error}")
    return elapsed


def percentile(values: list[float], fraction: float) -> float:
    ordered = sorted(values)
    index = min(int(len(ordered) * fraction), len(ordered) - 1)
    return ordered[index]


async def main() -> None:
    settings = ItmanoCrmSettings()
    async with ItmanoCrmClient(settings) as client:
        identity = await client.verify()
        registry = ToolRegistry()
        register(registry, client)
        registry.freeze()

        print(f"tenant: {identity.tenant_id} ({identity.environment})")
        print(f"tools:  {len(registry)}   repeats: {REPEATS} (first call discarded as cold)\n")

        results: dict[str, list[float]] = {}
        for name, arguments in SAMPLES:
            await timed(registry, name, arguments)  # warm-up, not recorded
            results[name] = [await timed(registry, name, arguments) for _ in range(REPEATS)]

        print(f"| {'tool':26} | {'p50':>8} | {'p95':>8} | {'min':>8} |")
        print(f"| {'-' * 26} | {'-' * 8} | {'-' * 8} | {'-' * 8} |")
        for name, samples in results.items():
            print(
                f"| {name:26} | {statistics.median(samples):7.0f}ms "
                f"| {percentile(samples, 0.95):7.0f}ms | {min(samples):7.0f}ms |"
            )

        floor = statistics.median(results["itmano_crm.whoami"])
        leads = statistics.median(results["itmano_crm.list_leads"])
        print(
            f"\nauthentication floor (whoami, reads no business data): {floor:.0f}ms"
            f"\nlist_leads beyond that floor:                          {leads - floor:.0f}ms"
            f"\nshare of a leads call spent before the query starts:    {floor / leads:.0%}"
        )

        started = time.perf_counter()
        for name, arguments in TURN:
            await timed(registry, name, arguments)
        turn_ms = (time.perf_counter() - started) * 1000
        print(
            f"\na {len(TURN)}-call turn, sequential: {turn_ms:.0f}ms"
            f"\n  of which authentication toll: {floor * len(TURN):.0f}ms"
        )


if __name__ == "__main__":
    asyncio.run(main())
