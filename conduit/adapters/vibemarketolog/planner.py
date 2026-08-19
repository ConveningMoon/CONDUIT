"""A planner built on a text model that has no native function calling.

The platform's ``text_models`` take a prompt and return prose. There is no
``tools`` parameter and no structured-output mode, so tool calling here is done
the way it was done before native support existed: describe the tools, demand one
JSON object, and validate what comes back.

Say that plainly wherever it is described. It is a deliberate adaptation, not a
capability the catalogue claims.

Two things make it hold up:

- **Strict validation.** The reply is parsed into a pydantic model. Anything that
  is not a well-formed plan naming a real tool is treated as a failure, not
  bent into shape.
- **Exactly one retry**, with the parse error fed back. A hard cap, not a loop:
  an unbounded repair loop is a hole in the cost ceiling, and the guard cannot
  close it because a planner call is not a tool call.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

import structlog
from pydantic import BaseModel, ConfigDict, Field, JsonValue, ValidationError

from conduit.adapters.vibemarketolog.client import GenerationError, VibemarketologClient
from conduit.core.agent import Plan, PlanRequest, Role
from conduit.core.tools import ToolCall, ToolSpec

__all__ = ["FAILED_REPLY", "LlmPlanner", "build_system_prompt"]

log = structlog.get_logger(__name__)

FAILED_REPLY = (
    "I could not work out how to answer that. Try rephrasing it, "
    "or use a command — send /help for the list."
)

_FENCE = re.compile(r"^```(?:json)?\s*|\s*```$", re.MULTILINE)

INSTRUCTIONS = """You plan tool calls for an assistant working inside a CRM.

Reply with ONE JSON object and nothing else. No prose, no markdown fences.

{"reply": "<text for the user, or empty>", "tool_calls": [{"id": "<short id>", \
"name": "<exact tool name>", "arguments": {}}]}

Rules:
- Use tool_calls when you need data you do not have. Leave reply empty then.
- Use reply alone, with tool_calls empty, when you can answer from the \
conversation or when no tool can do what was asked.
- Never invent a tool name or an argument. Only what is listed below exists.
- If nothing listed can answer the question, say so in reply. Do not guess a \
call that might be close.
- LANGUAGE, and this outranks everything the data suggests: reply in the \
same language as the user's most recent message. The stored values are \
Spanish (perdido, media_alta) and must be kept verbatim, but the sentences \
around them follow the question. A Russian question gets a Russian answer; \
an English one gets English.

Available tools:
"""


class _PlannedCall(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = "call-1"
    name: str
    arguments: dict[str, JsonValue] = Field(default_factory=dict)


class _PlannerOutput(BaseModel):
    model_config = ConfigDict(extra="ignore")

    reply: str = ""
    tool_calls: list[_PlannedCall] = Field(default_factory=list)


def _render_tool(spec: ToolSpec) -> str:
    """One tool as the planner sees it: signature, purpose, per-argument notes.

    The argument notes are not padding. Everything an adapter knows about *how*
    to fill a field — which model to pay for and when, that an owner id has to be
    a real one, that a cursor only works with the filters that produced it —
    lives in the pydantic field description, and for a while none of it reached
    the model at all: only the tool-level sentence was sent. Rules written on
    individual arguments were dead weight, and the planner picked the cheapest
    image model every time regardless of whether the request needed legible text.

    The extra length costs almost nothing. The catalogue is byte-identical on
    every call, so the platform serves it from cache at a tenth of the input rate.
    """
    schema = spec.params.model_json_schema()
    properties: dict[str, Any] = schema.get("properties", {})
    required = set(schema.get("required", []))

    parts: list[str] = []
    notes: list[str] = []
    for name, definition in properties.items():
        detail = definition.get("enum") or definition.get("type") or "any"
        if isinstance(detail, list) and definition.get("enum"):
            detail = "|".join(str(value) for value in detail)
        marker = "" if name in required else "?"
        parts.append(f"{name}{marker}: {detail}")

        note = definition.get("description")
        if note:
            notes.append(f"      {name}: {note}")

    rendered = f"- {spec.name}({', '.join(parts)})\n    {spec.description}"
    if notes:
        rendered += "\n" + "\n".join(notes)
    return rendered


def build_system_prompt(tools: tuple[ToolSpec, ...]) -> str:
    return INSTRUCTIONS + "\n".join(_render_tool(spec) for spec in tools)


def _strip_fences(text: str) -> str:
    return _FENCE.sub("", text).strip()


MAX_RESULT_CHARS = 12000
"""How much of a tool result reaches the planner.

Generous on purpose. A page of ten leads is about 3000 characters — roughly 776
tokens, which at 60₽ per million input tokens is 0.05₽, below the per-call
minimum charge. Truncating to save that is throwing away data for nothing. The
earlier limit of 1500 cut a normal page in half, and the model correctly reported
that it could not see the rest.
"""


def _clip(content: str) -> str:
    """Trim only what is genuinely oversized, and say so when it happens.

    Silent truncation is the worst option: the model cannot tell a short list
    from a cut one, so it either invents the rest or hedges. An explicit marker
    lets it say "the first N" and be right.
    """
    if len(content) <= MAX_RESULT_CHARS:
        return content
    omitted = len(content) - MAX_RESULT_CHARS
    return (
        f"{content[:MAX_RESULT_CHARS]}\n"
        f"[truncated: {omitted} more characters. Tell the user the list is partial "
        f"and offer to narrow it with a filter.]"
    )


def _transcript(request: PlanRequest, limit: int = 12) -> str:
    lines: list[str] = []
    for turn in request.history[-limit:]:
        match turn.role:
            case Role.USER:
                lines.append(f"User: {turn.content}")
            case Role.ASSISTANT:
                lines.append(f"Assistant: {turn.content}")
            case Role.TOOL:
                lines.append(f"Result of {turn.tool_name}: {_clip(turn.content)}")
    return "\n".join(lines)


@dataclass(slots=True)
class LlmPlanner:
    """Turns a transcript plus a tool catalogue into the next step."""

    client: VibemarketologClient
    model: str | None = None
    known_tools: frozenset[str] = field(default_factory=frozenset)
    """Filled from the registry at startup. Kept separate from the prompt so a
    hallucinated name is caught by code, not only by the model's good behaviour."""

    async def plan(self, request: PlanRequest) -> Plan:
        system = build_system_prompt(request.tools)
        prompt = _transcript(request)
        names = self.known_tools or {spec.name for spec in request.tools}

        try:
            completion = await self.client.complete(system=system, prompt=prompt, model=self.model)
            parsed = self._parse(completion.text, names)
        except GenerationError as exc:
            log.warning("planner.generation_failed", error=str(exc))
            return Plan(reply=FAILED_REPLY)
        except ValueError as first_error:
            log.info("planner.reparse", reason=str(first_error)[:200])
            try:
                repair = await self.client.complete(
                    system=system,
                    prompt=(
                        f"{prompt}\n\nYour previous reply could not be used: {first_error}\n"
                        "Reply again with ONE valid JSON object and nothing else."
                    ),
                    model=self.model,
                    retry=True,
                )
                parsed = self._parse(repair.text, names)
            except (GenerationError, ValueError) as second_error:
                log.warning("planner.unusable", error=str(second_error)[:200])
                return Plan(reply=FAILED_REPLY)

        return Plan(
            reply=parsed.reply,
            tool_calls=tuple(
                ToolCall(id=item.id, name=item.name, arguments=item.arguments)
                for item in parsed.tool_calls
            ),
        )

    @staticmethod
    def _parse(text: str, known: set[str] | frozenset[str]) -> _PlannerOutput:
        """Strict. A near-miss is a failure, not something to bend into shape."""
        body = _strip_fences(text)
        if not body:
            raise ValueError("the reply was empty")

        try:
            raw = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ValueError(f"not valid JSON ({exc.msg})") from exc

        if not isinstance(raw, dict):
            raise ValueError("the top level must be a JSON object")

        try:
            output = _PlannerOutput.model_validate(raw)
        except ValidationError as exc:
            raise ValueError(
                f"does not match the required shape: {exc.error_count()} problem(s)"
            ) from exc

        unknown = [item.name for item in output.tool_calls if item.name not in known]
        if unknown:
            raise ValueError(f"no such tool: {', '.join(sorted(set(unknown)))}")

        if not output.tool_calls and not output.reply.strip():
            raise ValueError("neither a reply nor a tool call")

        return output
