"""Client for the platform's text generation endpoint.

``type=text`` is synchronous: the answer comes back in the same response, no
polling. Billing is per actual token — a reserve is held against ``max_tokens``
and the unused part is refunded in the same call, so the ``cost`` field is the
real figure, not an estimate.
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass
from types import TracebackType
from typing import Any, Self

import httpx

from conduit.adapters.vibemarketolog.config import VibemarketologSettings
from conduit.core.telemetry import ModelCall, record_model_call

__all__ = ["Completion", "GenerationError", "VibemarketologClient"]

_FINISHED = frozenset({"complete", "completed", "done", "success", "succeeded", "ready"})

_RESULT_KEYS = ("result_url", "result_urls", "file_url", "display_url", "url", "output")


def _has_result(payload: dict[str, Any]) -> bool:
    """A generation that has handed us a file is finished, whatever it is called."""
    return any(payload.get(key) for key in _RESULT_KEYS)


class GenerationError(RuntimeError):
    """The platform did not return a usable completion."""

    def __init__(self, message: str, *, status: int | None = None, retryable: bool = False) -> None:
        super().__init__(message)
        self.status = status
        self.retryable = retryable


@dataclass(frozen=True, slots=True)
class Completion:
    text: str
    model: str
    cost_rub: float
    latency_ms: int
    input_tokens: int
    output_tokens: int
    cached_tokens: int = 0


class VibemarketologClient:
    def __init__(
        self, settings: VibemarketologSettings, http: httpx.AsyncClient | None = None
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

    @property
    def _headers(self) -> dict[str, str]:
        return {"authorization": f"Bearer {self.settings.api_key.get_secret_value()}"}

    async def balance_rub(self) -> float:
        response = await self._http.get(
            f"{self.settings.base_url.rstrip('/')}/balance",
            headers=self._headers,
            timeout=self.settings.timeout_seconds,
        )
        response.raise_for_status()
        balance: float = response.json()["balance"]
        return balance

    async def complete(
        self,
        *,
        system: str,
        prompt: str,
        model: str | None = None,
        max_tokens: int | None = None,
        retry: bool = False,
    ) -> Completion:
        """One synchronous text generation, recorded in the turn ledger."""
        chosen = model or self.settings.planner_model
        body: dict[str, Any] = {
            "type": "text",
            "model": chosen,
            "system": system,
            "prompt": prompt,
            "max_tokens": max_tokens or self.settings.planner_max_tokens,
            "effort": self.settings.planner_effort,
        }

        started = time.perf_counter()
        try:
            response = await self._http.post(
                f"{self.settings.base_url.rstrip('/')}/generate",
                json=body,
                headers=self._headers,
                timeout=self.settings.planner_timeout_seconds,
            )
        except httpx.TimeoutException as exc:
            raise GenerationError(f"{chosen} timed out: {exc}", retryable=True) from exc
        except httpx.HTTPError as exc:
            raise GenerationError(f"cannot reach the platform: {exc}", retryable=True) from exc

        elapsed_ms = int((time.perf_counter() - started) * 1000)

        if not response.is_success:
            raise GenerationError(
                f"{chosen} returned {response.status_code}: {response.text[:200]}",
                status=response.status_code,
                retryable=response.status_code >= 500,
            )

        payload = response.json()
        usage = payload.get("usage") or {}
        completion = Completion(
            text=(payload.get("text") or "").strip(),
            model=chosen,
            cost_rub=float(payload.get("cost") or 0.0),
            latency_ms=elapsed_ms,
            input_tokens=int(usage.get("input") or 0),
            output_tokens=int(usage.get("output") or 0),
            cached_tokens=int(usage.get("cache_read") or 0),
        )
        record_model_call(
            ModelCall(
                model=completion.model,
                cost_rub=completion.cost_rub,
                latency_ms=completion.latency_ms,
                input_tokens=completion.input_tokens,
                output_tokens=completion.output_tokens,
                cached_tokens=completion.cached_tokens,
                retry=retry,
            )
        )
        return completion

    async def estimate(self, body: dict[str, Any]) -> dict[str, Any]:
        """Price and validate a generation without spending anything.

        Free, and the honest way to answer "what would that cost?". It is also
        the only way this adapter touches video at all.
        """
        response = await self._http.post(
            f"{self.settings.base_url.rstrip('/')}/generate/estimate",
            json=body,
            headers=self._headers,
            timeout=self.settings.timeout_seconds,
        )
        if not response.is_success:
            raise GenerationError(
                f"estimate rejected with {response.status_code}: {response.text[:200]}",
                status=response.status_code,
            )
        estimate: dict[str, Any] = response.json()
        return estimate

    async def start_generation(self, body: dict[str, Any]) -> str:
        """Begin a paid generation. Always strict: malformed params are rejected
        before the debit rather than after it."""
        payload = {**body, "strict": True}
        response = await self._http.post(
            f"{self.settings.base_url.rstrip('/')}/generate",
            json=payload,
            headers=self._headers,
            timeout=self.settings.timeout_seconds,
        )
        if not response.is_success:
            raise GenerationError(
                f"generation rejected with {response.status_code}: {response.text[:200]}",
                status=response.status_code,
                retryable=response.status_code >= 500,
            )
        started = response.json()
        generation_id = started.get("id") or started.get("generation_id")
        if not generation_id:
            raise GenerationError(f"no generation id in the reply: {str(started)[:200]}")
        return str(generation_id)

    async def await_generation(
        self, generation_id: str, *, poll_seconds: float = 3.0, timeout_seconds: float = 180.0
    ) -> dict[str, Any]:
        """Poll until the generation finishes, fails, or we give up waiting.

        Giving up is not the same as it failing: the work was paid for and may
        still complete, so the message says so rather than implying a refund.
        """
        deadline = time.monotonic() + timeout_seconds
        url = f"{self.settings.base_url.rstrip('/')}/generation/{generation_id}/status"

        while True:
            response = await self._http.get(
                url, headers=self._headers, timeout=self.settings.timeout_seconds
            )
            if not response.is_success:
                raise GenerationError(
                    f"status check returned {response.status_code}",
                    status=response.status_code,
                    retryable=True,
                )
            payload: dict[str, Any] = response.json()
            state = str(payload.get("status", "")).lower()

            # The observed terminal value is "complete" — not "completed", and not
            # "done". Matching a fixed vocabulary alone once cost 180 seconds of
            # polling an image that had been ready the whole time, so a produced
            # file also counts as finished, whatever the state is called.
            if state in _FINISHED or _has_result(payload):
                return payload
            if state in {"failed", "error", "cancelled", "canceled", "rejected"}:
                raise GenerationError(
                    f"generation {generation_id} finished as {state}: "
                    f"{str(payload.get('error') or payload.get('message') or '')[:200]}"
                )
            if time.monotonic() >= deadline:
                raise GenerationError(
                    f"generation {generation_id} was still {state or 'pending'} after "
                    f"{timeout_seconds:g}s. It was paid for and may yet finish; "
                    f"check its status rather than starting another.",
                    retryable=False,
                )
            await asyncio.sleep(poll_seconds)
