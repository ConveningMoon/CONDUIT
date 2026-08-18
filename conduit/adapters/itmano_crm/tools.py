"""Registration of the CRM tools into a :class:`ToolRegistry`.

Descriptions here are not documentation for people — they are the only thing the
planner sees about a tool. Where the CRM's shape is surprising, the surprise is
stated in the description, because the alternative is the model discovering it
through a failed call.

Side effects and timeouts are read from the vendored contract, never hardcoded.
"""

from __future__ import annotations

from typing import Any

from conduit.adapters.itmano_crm.client import CrmError, ItmanoCrmClient
from conduit.adapters.itmano_crm.contract import operation, operations
from conduit.adapters.itmano_crm.models import (
    CreateEmailDraftParams,
    CreateLeadParams,
    CreateNoteParams,
    GetDealParams,
    GetLeadParams,
    ListDealsParams,
    ListLeadsParams,
    NoParams,
    SearchParams,
    UpdateLeadParams,
)
from conduit.core.tools import (
    SideEffect,
    ToolContext,
    ToolRegistry,
    ToolResult,
    ToolSpec,
)

__all__ = ["NAMESPACE", "agent_tool_operations", "register"]

NAMESPACE = "itmano_crm"


def agent_tool_operations() -> list[str]:
    """Operation ids the contract marks as belonging in an agent's catalogue.

    ``/contacts`` is excluded there on purpose: it returns the same people as
    ``/leads`` with the same ids, and a planner shown both would count everyone
    twice.
    """
    return sorted(op_id for op_id, op in operations().items() if op.agent_tool)


async def _run(
    client: ItmanoCrmClient,
    operation_id: str,
    *,
    path_params: dict[str, str] | None = None,
    query: dict[str, Any] | None = None,
    body: dict[str, Any] | None = None,
    idempotency_key: str | None = None,
) -> ToolResult:
    """Perform a call and flatten every expected failure into a result."""
    try:
        response = await client.call(
            operation_id,
            path_params=path_params,
            query=query,
            body=body,
            idempotency_key=idempotency_key,
        )
    except CrmError as exc:
        return ToolResult.failed(exc.code, exc.message, retryable=exc.retryable)
    return ToolResult.ok(response.data)


def _spec(
    name: str,
    operation_id: str,
    description: str,
    params: type[Any],
    client: ItmanoCrmClient,
) -> ToolSpec:
    op = operation(operation_id)
    return ToolSpec(
        name=f"{NAMESPACE}.{name}",
        description=description,
        params=params,
        side_effect=SideEffect.WRITE if op.is_write else SideEffect.READ,
        timeout_seconds=op.timeout_seconds(client.settings.timeout_seconds),
    )


def register(registry: ToolRegistry, client: ItmanoCrmClient) -> None:
    """Publish the CRM tools. Call once at startup, before ``registry.freeze()``.

    The caller is responsible for having run :meth:`ItmanoCrmClient.verify`
    first: registering tools against an unverified deployment is how an agent
    ends up reading the wrong tenant.
    """

    async def whoami(ctx: ToolContext, params: NoParams) -> ToolResult:
        return await _run(client, "whoami")

    async def metadata(ctx: ToolContext, params: NoParams) -> ToolResult:
        return await _run(client, "getMetadata")

    async def list_leads(ctx: ToolContext, params: ListLeadsParams) -> ToolResult:
        return await _run(
            client, "listLeads", query=params.model_dump(exclude_none=True, mode="json")
        )

    async def get_lead(ctx: ToolContext, params: GetLeadParams) -> ToolResult:
        return await _run(client, "getLead", path_params={"id": params.id})

    async def list_deals(ctx: ToolContext, params: ListDealsParams) -> ToolResult:
        return await _run(
            client, "listDeals", query=params.model_dump(exclude_none=True, mode="json")
        )

    async def get_deal(ctx: ToolContext, params: GetDealParams) -> ToolResult:
        return await _run(client, "getDeal", path_params={"id": params.id})

    async def search(ctx: ToolContext, params: SearchParams) -> ToolResult:
        return await _run(client, "search", query=params.model_dump(mode="json"))

    async def create_lead(ctx: ToolContext, params: CreateLeadParams) -> ToolResult:
        return await _run(
            client,
            "createLead",
            body=params.model_dump(exclude_none=True, mode="json"),
            idempotency_key=ctx.idempotency_key,
        )

    async def update_lead(ctx: ToolContext, params: UpdateLeadParams) -> ToolResult:
        body = params.model_dump(exclude_none=True, mode="json")
        body.pop("id", None)
        return await _run(
            client,
            "updateLead",
            path_params={"id": params.id},
            body=body,
            idempotency_key=ctx.idempotency_key,
        )

    async def create_note(ctx: ToolContext, params: CreateNoteParams) -> ToolResult:
        return await _run(
            client,
            "createNote",
            body=params.model_dump(mode="json"),
            idempotency_key=ctx.idempotency_key,
        )

    async def draft_email(ctx: ToolContext, params: CreateEmailDraftParams) -> ToolResult:
        return await _run(
            client,
            "createEmailDraft",
            body=params.model_dump(mode="json"),
            idempotency_key=ctx.idempotency_key,
        )

    registry.register(
        _spec(
            "whoami",
            "whoami",
            "Report which tenant and environment this connection is bound to. "
            "Reads no business data. Useful to confirm wiring, not to answer questions.",
            NoParams,
            client,
        ),
        whoami,
    )
    registry.register(
        _spec(
            "metadata",
            "getMetadata",
            "The values this CRM uses: funnel stages, quality bands, urgencies, "
            "pipelines, agent ids to use as 'owner', channels and currency. Call it "
            "when someone asks what values exist, and before creating a lead, which "
            "needs a real agent id. Do NOT call it as a preliminary step before "
            "filtering: every tool that accepts a stage already lists the valid "
            "stages in its own signature, so filter directly. This CRM has no custom "
            "fields; that list is always empty.",
            NoParams,
            client,
        ),
        metadata,
    )
    registry.register(
        _spec(
            "list_leads",
            "listLeads",
            "List leads for the tenant, newest first. A lead IS the person in this "
            "CRM — there is no separate contact record, so do not look for one. "
            "Returns a page plus next_cursor; pass that cursor back with identical "
            "filters to continue.",
            ListLeadsParams,
            client,
        ),
        list_leads,
    )
    registry.register(
        _spec(
            "get_lead",
            "getLead",
            "Fetch one lead in full, including score breakdown, quality band and "
            "urgency. Use after list_leads or search has given you an id.",
            GetLeadParams,
            client,
        ),
        get_lead,
    )
    registry.register(
        _spec(
            "list_deals",
            "listDeals",
            "List purchase processes. IMPORTANT: 'amount' is always null — this CRM "
            "does not record a deal value. The only money available is "
            "lead_budget_amount, which is the budget of the lead that owns the "
            "process, not the value of the deal. Never present it as a deal amount "
            "or add these up into a pipeline total.",
            ListDealsParams,
            client,
        ),
        list_deals,
    )
    registry.register(
        _spec(
            "get_deal",
            "getDeal",
            "Fetch one purchase process: address, loan type, closing date and notes. "
            "Same caveat as list_deals — there is no deal amount.",
            GetDealParams,
            client,
        ),
        get_deal,
    )
    registry.register(
        _spec(
            "search",
            "search",
            "Free-text search across leads, properties and deals. Returns type, id "
            "and a display label only — follow up with get_lead or get_deal for "
            "detail. Use this ONLY when you have a name or a fragment and no id. "
            "Anything shaped like 'demo-lead-003' is already an id: pass it straight "
            "to the tool that needs it instead of searching for it.",
            SearchParams,
            client,
        ),
        search,
    )
    registry.register(
        _spec(
            "create_lead",
            "createLead",
            "Create a lead. 'owner' is required: this CRM has no unassigned state, so "
            "get a valid agent id from metadata first. Creating a lead runs the "
            "normal intake pipeline, including scoring.",
            CreateLeadParams,
            client,
        ),
        create_lead,
    )
    registry.register(
        _spec(
            "update_lead",
            "updateLead",
            "Change a lead's funnel stage or its owner. This is the ONLY way to move "
            "a stage — there is no separate deal-stage operation, and moving a deal "
            "means moving the stage of the lead that owns it. The change is recorded "
            "in the lead's status history.",
            UpdateLeadParams,
            client,
        ),
        update_lead,
    )
    registry.register(
        _spec(
            "create_note",
            "createNote",
            "Attach a note to a lead or to a purchase process. Recorded as an event "
            "on the lead and does not affect its score. Use it to leave a record of "
            "what was said or agreed.",
            CreateNoteParams,
            client,
        ),
        create_note,
    )
    registry.register(
        _spec(
            "draft_email",
            "createEmailDraft",
            "Save an email draft against a lead. The CRM stores the subject and body "
            "verbatim and NEVER sends them — you are writing a draft for a person to "
            "review, so write the full final text.",
            CreateEmailDraftParams,
            client,
        ),
        draft_email,
    )
