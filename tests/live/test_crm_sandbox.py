"""Live checks against the CRM sandbox. Read-only, and skipped by default.

These are excluded from the normal suite (`-m 'not live'`) for two reasons: they
need credentials, and they need an egress the platform in front of the CRM does
not challenge. Development machines behind a VPN typically do not qualify, which
is exactly why this runs in CI instead.

Nothing here writes. The write surface stays untouched until the guard lands.
"""

from __future__ import annotations

import os

import pytest

from conduit.adapters.itmano_crm import CrmError, ItmanoCrmClient, ItmanoCrmSettings
from conduit.adapters.itmano_crm.contract import operations
from conduit.core.tools import ToolErrorCode

pytestmark = [
    pytest.mark.live,
    pytest.mark.skipif(
        not os.getenv("ITMANO_CRM_TOKEN"),
        reason="ITMANO_CRM_TOKEN is not set",
    ),
]


@pytest.fixture
async def client():
    settings = ItmanoCrmSettings()  # type: ignore[call-arg]
    async with ItmanoCrmClient(settings) as crm:
        yield crm


async def test_identity_matches_what_we_expect(client: ItmanoCrmClient) -> None:
    identity = await client.verify()

    assert identity.tenant_id == client.settings.expected_tenant
    assert identity.environment == client.settings.expected_environment
    assert "read" in identity.scopes


async def test_reading_leads_returns_the_demo_tenant(client: ItmanoCrmClient) -> None:
    response = await client.call("listLeads", query={"limit": 3})

    assert response.status == 200
    assert isinstance(response.data, dict)
    rows = response.data["data"]
    assert isinstance(rows, list)
    assert len(rows) == 3
    # The demo tenant is synthetic. If this ever fails, something is very wrong.
    for row in rows:
        assert isinstance(row, dict)
        assert str(row["email"]).endswith("@example.com")


async def test_rate_limit_headers_are_present(client: ItmanoCrmClient) -> None:
    response = await client.call("whoami")

    assert response.rate_limit_remaining is not None


async def test_an_unknown_lead_maps_to_not_found(client: ItmanoCrmClient) -> None:
    with pytest.raises(CrmError) as caught:
        await client.call("getLead", path_params={"id": "demo-lead-does-not-exist"})

    assert caught.value.code is ToolErrorCode.NOT_FOUND
    assert caught.value.retryable is False


async def test_an_over_large_limit_is_rejected_not_truncated(client: ItmanoCrmClient) -> None:
    with pytest.raises(CrmError) as caught:
        await client.call("listLeads", query={"limit": 500})

    assert caught.value.code is ToolErrorCode.INVALID_ARGUMENTS


async def test_the_served_contract_still_matches_the_vendored_copy(
    client: ItmanoCrmClient,
) -> None:
    """Drift detector.

    The vendored contract is where per-operation timeouts and the agent-tool
    filter come from. If the server's copy moves, this adapter is reasoning from
    a stale document and needs to be re-vendored.
    """
    live = await client.fetch_served_contract()

    live_ids = {
        spec["operationId"]
        for item in live["paths"].values()
        for method, spec in item.items()
        if method in {"get", "post", "patch", "put", "delete"}
    }
    assert live_ids == set(operations())
