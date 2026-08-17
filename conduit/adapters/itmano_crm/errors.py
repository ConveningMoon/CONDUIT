"""Translation from the CRM's error vocabulary into CONDUIT's.

The CRM publishes a stable ``code`` string alongside the HTTP status, which is
what this maps. Status codes are only the fallback for a response that never
reached the application — a proxy 502, an edge timeout — where there is no
envelope to read.
"""

from __future__ import annotations

from conduit.core.tools import ToolErrorCode

__all__ = ["RETRYABLE_STATUSES", "from_code", "from_status"]

_BY_CODE: dict[str, tuple[ToolErrorCode, bool]] = {
    "invalid_arguments": (ToolErrorCode.INVALID_ARGUMENTS, False),
    "unauthorized": (ToolErrorCode.UNAUTHORIZED, False),
    "insufficient_scope": (ToolErrorCode.UNAUTHORIZED, False),
    "not_found": (ToolErrorCode.NOT_FOUND, False),
    "unprocessable": (ToolErrorCode.INVALID_ARGUMENTS, False),
    "rate_limited": (ToolErrorCode.RATE_LIMITED, True),
    "upstream_error": (ToolErrorCode.UPSTREAM_ERROR, True),
    "timeout": (ToolErrorCode.TIMEOUT, True),
    # Reusing a key with a different body is a caller bug, not a transient fault.
    "idempotency_key_reuse": (ToolErrorCode.INVALID_ARGUMENTS, False),
    # Same key still in flight: retryable, but it is not a quota problem. Calling
    # it RATE_LIMITED would earn it the guard's long backoff for something that
    # clears in milliseconds.
    "idempotency_key_in_flight": (ToolErrorCode.UPSTREAM_ERROR, True),
}

_BY_STATUS: dict[int, tuple[ToolErrorCode, bool]] = {
    400: (ToolErrorCode.INVALID_ARGUMENTS, False),
    401: (ToolErrorCode.UNAUTHORIZED, False),
    403: (ToolErrorCode.UNAUTHORIZED, False),
    404: (ToolErrorCode.NOT_FOUND, False),
    409: (ToolErrorCode.INVALID_ARGUMENTS, False),
    422: (ToolErrorCode.INVALID_ARGUMENTS, False),
    429: (ToolErrorCode.RATE_LIMITED, True),
    500: (ToolErrorCode.UPSTREAM_ERROR, True),
    502: (ToolErrorCode.UPSTREAM_ERROR, True),
    503: (ToolErrorCode.UPSTREAM_ERROR, True),
    504: (ToolErrorCode.TIMEOUT, True),
}

RETRYABLE_STATUSES = frozenset(status for status, (_, retry) in _BY_STATUS.items() if retry)


def from_code(code: str, status: int) -> tuple[ToolErrorCode, bool]:
    """Map a published error code. Falls back to the status when unrecognised.

    An unknown code means the contract moved under us. That is not something to
    retry blindly, so the fallback deliberately does not invent retryability the
    status does not already justify.
    """
    known = _BY_CODE.get(code)
    if known is not None:
        return known
    return from_status(status)


def from_status(status: int) -> tuple[ToolErrorCode, bool]:
    return _BY_STATUS.get(status, (ToolErrorCode.UPSTREAM_ERROR, False))
