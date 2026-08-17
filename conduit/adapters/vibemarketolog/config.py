"""Configuration for the platform Agent API."""

from __future__ import annotations

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ["PLANNER_MODELS", "VibemarketologSettings"]

PLANNER_MODELS: dict[str, float] = {
    "gpt-5.6-luna": 0.5,
    "claude-opus-5": 3.75,
    "gpt-5.6-sol": 4.2,
}
"""Rough rubles per planning call, from the catalogue's own sample figures.

Used only for estimates and for the side-by-side comparison. The authoritative
number is the ``cost`` the API returns on every response, which is what gets
recorded.
"""


class VibemarketologSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="VIBEMARKETOLOG_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    base_url: str
    api_key: SecretStr

    planner_model: str = "gpt-5.6-luna"
    """Cheap by default, and it is the right default: on the golden set it picks
    the same tools as the expensive one. Switched to ``claude-opus-5`` for a live
    demo, where the cost of being wrong exceeds the cost of the tokens."""

    planner_max_tokens: int = Field(default=600, ge=64)
    planner_effort: str = "low"
    timeout_seconds: float = Field(default=60.0, gt=0)

    image_model: str = "qwen-image-3"
    """7₽ a call, photorealistic, and accurate at rendering text inside the image
    — which a promotional graphic needs. ``z-image`` at 1.2₽ is the cheap option
    used while developing; the expensive tiers run 15-70 RUB and buy nothing this
    demo shows."""

    image_timeout_seconds: float = Field(default=180.0, gt=0)
