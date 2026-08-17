"""Configuration for the ITMANO CRM adapter. Everything arrives via env vars."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["ItmanoCrmSettings"]


class ItmanoCrmSettings(BaseSettings):
    """Connection details plus the assertion that guards against pointing here
    at the wrong place.

    ``expected_tenant`` and ``expected_environment`` are not decoration. The
    adapter calls ``/whoami`` before publishing a single tool and refuses to
    start if either disagrees. A deployment wired to the wrong tenant has to
    fail loudly; the alternative is an agent quietly reading someone else's
    business.
    """

    model_config = SettingsConfigDict(
        env_prefix="ITMANO_CRM_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str
    token: SecretStr
    expected_tenant: str
    expected_environment: str = "sbx"

    timeout_seconds: float = Field(default=15.0, gt=0.0)
    """Ceiling for any single call. Per-operation timeouts come from the
    contract's ``x-itmano-deadline-ms`` and are capped by this."""

    @property
    def api_root(self) -> str:
        return f"{self.base_url.rstrip('/')}/api"
