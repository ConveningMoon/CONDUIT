"""Adapter for the ITMANO CRM agent surface (``/agent/v1``).

The CRM owns tenant isolation. The bearer token CONDUIT presents is exchanged
server-side for a real database session, so row level security decides what
comes back — no request from here ever carries a tenant identifier, and there is
nothing this adapter could get wrong that would widen its own access.
"""

from conduit.adapters.itmano_crm.client import CrmError, CrmResponse, ItmanoCrmClient, WhoAmI
from conduit.adapters.itmano_crm.config import ItmanoCrmSettings
from conduit.adapters.itmano_crm.contract import Operation, operation, operations

__all__ = [
    "CrmError",
    "CrmResponse",
    "ItmanoCrmClient",
    "ItmanoCrmSettings",
    "Operation",
    "WhoAmI",
    "operation",
    "operations",
]
