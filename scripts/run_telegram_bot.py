"""Wire the whole thing together and long-poll Telegram.

Startup order matters and is deliberate:

1. Load the binding file. No bindings, no start.
2. Verify the CRM connection reports the tenant and environment we expect.
3. Only then register tools, and freeze the registry.

Every step fails closed. A bot that starts anyway and discovers at message time
that it is pointed at the wrong tenant has already lost.
"""

from __future__ import annotations

import asyncio
import logging
import sys

import structlog

from conduit.adapters.itmano_crm import ItmanoCrmClient, ItmanoCrmSettings
from conduit.adapters.itmano_crm.tools import register
from conduit.core.agent import Agent, ReadOnlyGuard
from conduit.core.tools import ToolRegistry
from conduit.interfaces.telegram import CommandPlanner, TelegramSettings, load_bindings
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
    try:
        identity = await crm.verify()
        log.info(
            "crm.verified",
            tenant=identity.tenant_id,
            environment=identity.environment,
            scopes=identity.scopes,
        )

        unbound = bindings.tenants - {identity.tenant_id}
        if unbound:
            # A binding pointing somewhere the token cannot reach would fail one
            # message at a time, confusingly. Say it once, at startup.
            log.error("bindings.unreachable_tenants", tenants=sorted(unbound))
            return 1

        registry = ToolRegistry()
        register(registry, crm)
        registry.freeze()
        log.info("tools.registered", count=len(registry))

        agent = Agent(
            registry=registry,
            planner=CommandPlanner(),
            guard=ReadOnlyGuard(),
        )
        await run(agent, bindings, telegram)
    finally:
        await crm.aclose()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
