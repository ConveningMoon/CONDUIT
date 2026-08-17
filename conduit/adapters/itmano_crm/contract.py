"""The published contract, vendored.

``contract/openapi.json`` is a byte-for-byte copy of what the CRM serves at
``/api/agent/v1/openapi.json``. Reading it rather than hardcoding routes buys
three things: per-operation timeouts that cannot drift from the deadlines the
server actually enforces, the ``x-itmano-agent-tool`` filter that keeps
``/contacts`` out of the planner's catalogue, and a drift test that fails when
the live document moves.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import cache
from importlib import resources
from typing import Any

__all__ = ["Operation", "contract_version", "load_contract", "operation", "operations"]

CONTRACT_RESOURCE = "contract/openapi.json"

TIMEOUT_MARGIN_SECONDS = 5.0
"""Added on top of the server deadline.

The client timeout must sit *above* the server's, or we abandon the request just
as it is about to answer and swap their structured 504 for our own blind one.
"""

_HTTP_METHODS = frozenset({"get", "post", "patch", "put", "delete"})


@dataclass(frozen=True, slots=True)
class Operation:
    """One route, as the contract describes it."""

    operation_id: str
    method: str
    path: str
    agent_tool: bool
    scope: str
    deadline_ms: int

    @property
    def is_write(self) -> bool:
        return self.scope == "write"

    def timeout_seconds(self, ceiling: float) -> float:
        """Client-side timeout: the server's deadline plus room to answer."""
        return min(self.deadline_ms / 1000.0 + TIMEOUT_MARGIN_SECONDS, ceiling)

    def format_path(self, path_params: dict[str, str] | None = None) -> str:
        if not path_params:
            return self.path
        return self.path.format(**path_params)


@cache
def load_contract() -> dict[str, Any]:
    """Parse the vendored document. Cached; the file cannot change at runtime."""
    source = resources.files("conduit.adapters.itmano_crm").joinpath(CONTRACT_RESOURCE)
    parsed: dict[str, Any] = json.loads(source.read_text(encoding="utf-8"))
    return parsed


def contract_version() -> str:
    info: dict[str, Any] = load_contract()["info"]
    version: str = info["version"]
    return version


@cache
def operations() -> dict[str, Operation]:
    """Every operation in the contract, keyed by ``operationId``."""
    found: dict[str, Operation] = {}
    paths: dict[str, Any] = load_contract()["paths"]
    for path, item in paths.items():
        for method, spec in item.items():
            if method not in _HTTP_METHODS:
                continue
            operation_id = spec["operationId"]
            found[operation_id] = Operation(
                operation_id=operation_id,
                method=method.upper(),
                path=path,
                agent_tool=bool(spec.get("x-itmano-agent-tool", False)),
                scope=str(spec.get("x-itmano-scope", "read")),
                deadline_ms=int(spec.get("x-itmano-deadline-ms", 5000)),
            )
    return found


def operation(operation_id: str) -> Operation:
    try:
        return operations()[operation_id]
    except KeyError:
        raise KeyError(f"{operation_id!r} is not in the published contract") from None
