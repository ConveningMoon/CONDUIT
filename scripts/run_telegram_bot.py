"""Wire the whole thing together and long-poll Telegram.

Startup order matters and is deliberate:

1. Load the binding file. No bindings, no start.
2. Verify the CRM connection reports the tenant and environment we expect.
3. Only then register tools, and freeze the registry.

Every step fails closed. A bot that starts anyway and discovers at message time
that it is pointed at the wrong tenant has already lost.

**One instance only.** The guard's counters are in process memory, so a second
replica would keep its own ceilings and neither would be a ceiling.
"""

from __future__ import annotations

import asyncio
import logging
import sys

import structlog

from conduit.adapters.itmano_crm import ItmanoCrmClient, ItmanoCrmSettings
from conduit.adapters.itmano_crm.tools import register
from conduit.adapters.vibemarketolog import (
    LlmPlanner,
    VibemarketologClient,
    VibemarketologSettings,
)
from conduit.adapters.vibemarketolog import register as register_generation
from conduit.core.agent import Agent
from conduit.core.audit import HashChainAuditSink, InMemoryAuditStore
from conduit.core.guard import DeterministicGuard, GuardSettings, InMemoryGuardStore
from conduit.core.tools import SideEffect, ToolRegistry
from conduit.interfaces.telegram import CommandFastPath, TelegramSettings, load_bindings
from conduit.interfaces.telegram.bot import run

log = structlog.get_logger("conduit")


async def main() -> int:
    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=logging.INFO)

    telegram = TelegramSettings()
    bindings = load_bindings(telegram.bindings_path)
    log.info(
        "bindings.loaded",
        path=str(telegram.bindings_path),
        chats=len(bindings),
        tenants=sorted(bindings.tenants),
    )

    crm = ItmanoCrmClient(ItmanoCrmSettings())
    platform = VibemarketologClient(VibemarketologSettings())
    try:
        registry = ToolRegistry()

        # The CRM check is the authorization boundary and still fails closed —
        # but it fails closed on the CRM *tools*, not on the whole process. If
        # the CRM cannot be verified, its tools are simply never registered, so
        # nothing can call them; generation still works. Refusing to start at all
        # would throw away the half of the system that is fine.
        try:
            identity = await crm.verify()
            unbound = bindings.tenants - {identity.tenant_id}
            if unbound:
                log.error("bindings.unreachable_tenants", tenants=sorted(unbound))
                return 1
            register(registry, crm)
            log.info(
                "crm.verified",
                tenant=identity.tenant_id,
                environment=identity.environment,
                scopes=identity.scopes,
            )
        except Exception as exc:
            log.error(
                "crm.unavailable",
                error=str(exc)[:200],
                consequence="CRM tools are NOT registered and cannot be called; "
                "generation still works",
            )

        register_generation(registry, platform)
        registry.freeze()

        # Every read, plus exactly one write we chose to allow. Generation spends
        # money, so it is a WRITE and has to be named here to happen at all; a CRM
        # write is not on the list and is refused by rule, not by luck.
        whitelist = frozenset(
            spec.name
            for spec in registry.specs()
            if spec.side_effect is SideEffect.READ or spec.name == "vibemarketolog.generate_image"
        )
        log.info(
            "tools.registered",
            count=len(registry),
            allowed=len(whitelist),
            denied=sorted({spec.name for spec in registry.specs()} - whitelist),
        )

        # Informational, and deliberately NOT fatal. The CRM check above is the
        # authorization boundary and must fail closed; this one is a courtesy. If
        # the generation API is down, the command fast path still answers every
        # /leads and /lead, which is exactly the safety net that would be wasted
        # by refusing to start.
        try:
            log.info(
                "planner.ready",
                model=platform.settings.planner_model,
                balance_rub=await platform.balance_rub(),
            )
        except Exception as exc:
            log.warning(
                "planner.unreachable",
                error=str(exc)[:200],
                consequence="commands still work; free-form questions will not",
            )

        agent = Agent(
            registry=registry,
            planner=CommandFastPath(
                fallback=LlmPlanner(
                    client=platform,
                    known_tools=frozenset(spec.name for spec in registry.specs()),
                )
            ),
            guard=DeterministicGuard(
                settings=GuardSettings(allow_writes=True, whitelist=whitelist),
                store=InMemoryGuardStore(),
            ),
            audit=HashChainAuditSink(store=InMemoryAuditStore()),
        )
        await run(agent, bindings, telegram)
    finally:
        await crm.aclose()
        await platform.aclose()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
