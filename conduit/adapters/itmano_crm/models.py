"""Argument models for the CRM tools.

Every enum here is copied from the vendored contract rather than invented. The
planner sees these as JSON schema, so a wrong value costs a round trip and an
``invalid_arguments`` it could have avoided.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated, Any, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

__all__ = [
    "CreateEmailDraftParams",
    "CreateLeadParams",
    "CreateNoteParams",
    "GetDealParams",
    "GetLeadParams",
    "Intent",
    "Language",
    "LeadStage",
    "ListDealsParams",
    "ListLeadsParams",
    "NoParams",
    "NoteTarget",
    "SearchParams",
    "UpdateLeadParams",
]


class LeadStage(StrEnum):
    """Funnel stage. Moved by a person, never by the system."""

    NUEVO = "nuevo"
    NUTRICION = "nutricion"
    EN_PROCESO = "en_proceso"
    CERRADO = "cerrado"
    PERDIDO = "perdido"


_STAGE_ALIASES: dict[str, str] = {
    "new": "nuevo",
    "nurturing": "nutricion",
    "nurture": "nutricion",
    "in_progress": "en_proceso",
    "in progress": "en_proceso",
    "closed": "cerrado",
    "won": "cerrado",
    "lost": "perdido",
}
"""English names a planner reaches for, mapped onto the values the CRM stores.

Measured, not imagined: on the golden set both models emitted ``lost`` for
"perdido" and ``closed`` for "cerrado". Rejecting those costs a whole extra
planning round trip — the model reads INVALID_ARGUMENTS, corrects itself and
tries again, so a turn that should take two model calls takes three.

This normalises the request. It does not invent data: every alias maps to a value
the CRM already defines, and anything unrecognised is still rejected.
"""


def _normalise_stage(value: Any) -> Any:
    if isinstance(value, str):
        key = value.strip().casefold().replace("-", "_")
        return _STAGE_ALIASES.get(key, value)
    return value


Stage = Annotated[LeadStage, BeforeValidator(_normalise_stage)]


class Language(StrEnum):
    ES = "es"
    EN = "en"
    PT = "pt"


class Intent(StrEnum):
    BUY = "buy"
    INVEST = "invest"
    SELL = "sell"


class NoteTarget(StrEnum):
    LEAD = "lead"
    CONTACT = "contact"
    DEAL = "deal"


class _Params(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")


class NoParams(_Params):
    """For tools that take no arguments."""


class ListLeadsParams(_Params):
    stage: Stage | None = Field(default=None, description="Filter by funnel stage.")
    owner: str | None = Field(
        default=None,
        description="Agent id that owns the lead. Valid ids come from itmano_crm.metadata.",
    )
    created_after: str | None = Field(
        default=None,
        description="ISO 8601 date or timestamp. Only leads created after it.",
    )
    q: str | None = Field(default=None, description="Free-text search over name, email and phone.")
    limit: int = Field(default=25, ge=1, le=100)
    cursor: str | None = Field(
        default=None,
        description=(
            "Opaque cursor from a previous page. Only valid with the SAME filters that produced it."
        ),
    )


class GetLeadParams(_Params):
    id: str = Field(
        min_length=1,
        description="Opaque lead id. Not a uuid — do not assume any format.",
    )


class ListDealsParams(_Params):
    lead_stage: Stage | None = Field(
        default=None,
        description="Stage of the lead that owns the purchase process.",
    )
    pipeline: Literal["compra"] | None = None
    min_lead_budget: float | None = Field(
        default=None,
        ge=0,
        description="Minimum budget of the owning lead, not of the deal.",
    )
    close_before: str | None = Field(
        default=None,
        description="ISO 8601 date. Deals with no closing date are excluded.",
    )
    limit: int = Field(default=25, ge=1, le=100)
    cursor: str | None = None


class GetDealParams(_Params):
    id: str = Field(min_length=1, description="Deal id. This one is a uuid.")


class SearchParams(_Params):
    q: str = Field(min_length=1, description="Free text. Searches leads, properties and deals.")
    limit: int = Field(default=10, ge=1, le=25)


class CreateLeadParams(_Params):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(default="", max_length=100)
    email: str = Field(max_length=255)
    owner: str = Field(
        min_length=1,
        max_length=64,
        description=(
            "Agent id that will own the lead. REQUIRED: the CRM has no unassigned "
            "state. Call itmano_crm.metadata first to get a valid id."
        ),
    )
    language: Language = Language.ES
    phone: str | None = Field(default=None, max_length=30)
    intent: Intent | None = None
    budget_amount: float | None = Field(default=None, ge=0)
    notes: str | None = Field(default=None, max_length=4000)


class UpdateLeadParams(_Params):
    id: str = Field(min_length=1)
    stage: Stage | None = Field(
        default=None,
        description="New funnel stage. The change is recorded in the lead's status history.",
    )
    owner: str | None = Field(default=None, min_length=1, max_length=64)


class CreateNoteParams(_Params):
    target_type: NoteTarget = Field(
        description=(
            "'contact' resolves to the same lead; 'deal' resolves to the lead that "
            "owns the purchase process."
        )
    )
    target_id: str = Field(min_length=1, max_length=64)
    body: str = Field(min_length=1, max_length=4000)


class CreateEmailDraftParams(_Params):
    lead_id: str = Field(min_length=1, max_length=64)
    subject: str = Field(min_length=1, max_length=500)
    body: str = Field(
        min_length=1,
        max_length=50000,
        description="Full draft body. The CRM stores it verbatim and never sends it.",
    )
