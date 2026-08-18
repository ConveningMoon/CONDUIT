"""HTTP client for the CRM agent surface.

Failures raise :class:`CrmError` carrying an already-translated
:class:`~conduit.core.tools.ToolErrorCode`. The tool handlers convert those into
``ToolResult`` values, so nothing escapes the adapter as an exception — and if
something ever did, ``ToolRegistry.invoke`` catches it anyway.
"""

from __future__ import annotations

import asyncio
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Self

import httpx
import structlog
from pydantic import BaseModel, ConfigDict, JsonValue

from conduit.adapters.itmano_crm import errors
from conduit.adapters.itmano_crm.config import ItmanoCrmSettings
from conduit.adapters.itmano_crm.contract import Operation, contract_version, operation
from conduit.core.tools import ToolErrorCode

__all__ = ["CrmError", "CrmResponse", "ItmanoCrmClient", "WhoAmI"]

log = structlog.get_logger(__name__)


class CrmError(Exception):
    """A call that did not succeed, already in CONDUIT's error vocabulary."""

    def __init__(
        self,
        code: ToolErrorCode,
        message: str,
        *,
        retryable: bool = False,
        status: int | None = None,
        crm_code: str | None = None,
        retry_after_seconds: float | None = None,
        mitigated: bool = False,
    ) -> None:
        super().__init__(message)
        self.mitigated = mitigated
        """True when the platform in front of the CRM answered instead of the CRM.
        Transient by nature, and worth retrying — unlike a real refusal."""
        self.code = code
        self.message = message
        self.retryable = retryable
        self.status = status
        self.crm_code = crm_code
        self.retry_after_seconds = retry_after_seconds
        """Only set on 429. The guard uses it instead of guessing a backoff."""


class ConfigurationError(RuntimeError):
    """The adapter is pointed somewhere it was not meant to reach."""


@dataclass(frozen=True, slots=True)
class CrmResponse:
    """A successful call, plus the headers worth carrying forward."""

    status: int
    data: JsonValue
    rate_limit_remaining: int | None = None
    idempotency_replayed: bool = False


class WhoAmI(BaseModel):
    """Identity the server reports for our token."""

    model_config = ConfigDict(frozen=True, extra="ignore")

    tenant: dict[str, str]
    scopes: list[str]
    api_version: str
    environment: str

    @property
    def tenant_id(self) -> str:
        return self.tenant["id"]

    @property
    def tenant_name(self) -> str:
        return self.tenant.get("name", "")

    @property
    def can_write(self) -> bool:
        return "write" in self.scopes


def _int_header(response: httpx.Response, name: str) -> int | None:
    raw = response.headers.get(name)
    if raw is None:
        return None
    try:
        return int(raw)
    except ValueError:
        return None


def _float_header(response: httpx.Response, name: str) -> float | None:
    raw = response.headers.get(name)
    if raw is None:
        return None
    try:
        return float(raw)
    except ValueError:
        return None


class ItmanoCrmClient:
    """One client per process. Holds the connection pool; owns no state."""

    def __init__(
        self,
        settings: ItmanoCrmSettings,
        http: httpx.AsyncClient | None = None,
    ) -> None:
        self.settings = settings
        self._owns_http = http is None
        self._http = http or httpx.AsyncClient()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        if self._owns_http:
            await self._http.aclose()

    def _headers(self, idempotency_key: str | None) -> dict[str, str]:
        headers = {
            "authorization": f"Bearer {self.settings.token.get_secret_value()}",
            "accept": "application/json",
            "user-agent": f"conduit-itmano-adapter/{contract_version()}",
        }
        if idempotency_key is not None:
            headers["idempotency-key"] = idempotency_key
        return headers

    async def call(
        self,
        operation_id: str,
        *,
        path_params: dict[str, str] | None = None,
        query: dict[str, Any] | None = None,
        body: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
    ) -> CrmResponse:
        """Perform one operation from the contract."""
        op: Operation = operation(operation_id)
        url = f"{self.settings.api_root}{op.format_path(path_params)}"
        params = {k: v for k, v in (query or {}).items() if v is not None}

        try:
            response = await self._http.request(
                op.method,
                url,
                params=params or None,
                json=body,
                headers=self._headers(idempotency_key),
                timeout=op.timeout_seconds(self.settings.timeout_seconds),
            )
        except httpx.TimeoutException as exc:
            raise CrmError(
                ToolErrorCode.TIMEOUT,
                f"{operation_id} timed out before the server answered: {exc}",
                retryable=True,
            ) from exc
        except httpx.HTTPError as exc:
            raise CrmError(
                ToolErrorCode.UPSTREAM_ERROR,
                f"{operation_id} could not reach the CRM: {exc}",
                retryable=True,
            ) from exc

        if response.is_success:
            return CrmResponse(
                status=response.status_code,
                data=self._decode(response, operation_id),
                rate_limit_remaining=_int_header(response, "x-ratelimit-remaining"),
                idempotency_replayed=response.headers.get("idempotency-replayed") == "true",
            )

        raise self._error(response, operation_id)

    def _decode(self, response: httpx.Response, operation_id: str) -> JsonValue:
        try:
            decoded: JsonValue = response.json()
        except ValueError as exc:
            raise CrmError(
                ToolErrorCode.UPSTREAM_ERROR,
                f"{operation_id} returned a body that is not JSON",
                retryable=False,
                status=response.status_code,
            ) from exc
        return decoded

    def _error(self, response: httpx.Response, operation_id: str) -> CrmError:
        status = response.status_code
        crm_code: str | None = None
        detail = response.reason_phrase or "no detail"

        # A challenge from the hosting platform is not the CRM refusing us. Saying
        # which one happened turns a confusing 403 into an obvious one.
        mitigation = response.headers.get("x-vercel-mitigated")
        if mitigation:
            return CrmError(
                ToolErrorCode.UPSTREAM_ERROR,
                f"{operation_id} never reached the CRM: the hosting platform "
                f"answered with a {mitigation!r} challenge ({status}).",
                retryable=True,
                status=status,
                mitigated=True,
            )

        try:
            payload = response.json()
        except ValueError:
            payload = None

        if isinstance(payload, dict) and isinstance(payload.get("error"), dict):
            envelope: dict[str, Any] = payload["error"]
            crm_code = str(envelope.get("code", "")) or None
            detail = str(envelope.get("message", detail))

        code, retryable = (
            errors.from_code(crm_code, status) if crm_code else errors.from_status(status)
        )
        return CrmError(
            code,
            f"{operation_id} failed with {status} {crm_code or 'unmapped'}: {detail}",
            retryable=retryable,
            status=status,
            crm_code=crm_code,
            retry_after_seconds=_float_header(response, "retry-after"),
        )

    async def fetch_served_contract(self) -> dict[str, Any]:
        """Download the contract the server is publishing right now.

        Used to detect drift against the vendored copy. This route needs no
        token, which is why it does not go through :meth:`call`.
        """
        url = f"{self.settings.api_root}/agent/v1/openapi.json"
        response = await self._http.get(url, timeout=self.settings.timeout_seconds)
        if not response.is_success:
            raise self._error(response, "getOpenApi")
        served: dict[str, Any] = response.json()
        return served

    async def whoami(self) -> WhoAmI:
        response = await self.call("whoami")
        return WhoAmI.model_validate(response.data)

    async def verify(self, *, attempts: int = 3, backoff_seconds: float = 2.0) -> WhoAmI:
        """Refuse to serve anything if the server is not who we expect.

        Called once before tools are registered. A mismatch here means the
        deployment is pointed at the wrong tenant or the wrong environment, and
        the only safe response is to not start.

        Retried, because the failure that actually happens is a transient
        challenge from the hosting platform rather than a real refusal, and one
        unlucky moment at startup should not cost the CRM tools for the whole
        run. A definite answer — wrong scope, bad token — is never retried.
        """
        for attempt in range(1, attempts + 1):
            try:
                identity = await self.whoami()
                break
            except CrmError as exc:
                worth_retrying = exc.mitigated or exc.retryable
                if attempt == attempts or not worth_retrying:
                    raise
                log.warning(
                    "crm.verify_retry",
                    attempt=attempt,
                    of=attempts,
                    error=str(exc)[:160],
                )
                await asyncio.sleep(backoff_seconds * attempt)
        else:  # pragma: no cover - the loop always breaks or raises
            raise CrmError(ToolErrorCode.UPSTREAM_ERROR, "verify exhausted its attempts")

        if attempt > 1:
            log.info("crm.verify_recovered", attempts=attempt)

        mismatches: list[str] = []
        if identity.tenant_id != self.settings.expected_tenant:
            mismatches.append(
                f"tenant is {identity.tenant_id!r}, expected {self.settings.expected_tenant!r}"
            )
        if identity.environment != self.settings.expected_environment:
            mismatches.append(
                f"environment is {identity.environment!r}, "
                f"expected {self.settings.expected_environment!r}"
            )

        if mismatches:
            raise ConfigurationError("refusing to register CRM tools: " + "; ".join(mismatches))
        return identity
