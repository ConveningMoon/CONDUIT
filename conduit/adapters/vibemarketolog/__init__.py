"""Adapter for the platform's Agent API.

Two roles, kept separate on purpose. The text models back the planner — the
agent's reasoning. Generation of images, video and audio will be tools like any
other, registered into the same registry the CRM uses.
"""

from conduit.adapters.vibemarketolog.client import (
    Completion,
    GenerationError,
    VibemarketologClient,
)
from conduit.adapters.vibemarketolog.config import PLANNER_MODELS, VibemarketologSettings
from conduit.adapters.vibemarketolog.planner import FAILED_REPLY, LlmPlanner, build_system_prompt
from conduit.adapters.vibemarketolog.tools import register

__all__ = [
    "FAILED_REPLY",
    "PLANNER_MODELS",
    "Completion",
    "GenerationError",
    "LlmPlanner",
    "VibemarketologClient",
    "VibemarketologSettings",
    "build_system_prompt",
    "register",
]
