"""A deterministic planner for explicit commands.

CONDUIT's orchestration loop expects a :class:`~conduit.core.agent.Planner`. A
language model is the interesting implementation, and it needs an API key this
project does not assume it has. This one needs nothing: it maps a slash command
onto exactly one tool call and renders the answer.

It is not a stand-in that will be thrown away. A messaging interface wants a
fast path for the handful of things people ask constantly, where spending a model
call to discover that ``/leads`` means "list the leads" is pure waste. When the
model-backed planner lands, this stays in front of it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any

from conduit.core.agent import Plan, Planner, PlanRequest, Role
from conduit.core.tools import SideEffect, ToolCall, ToolSpec

__all__ = ["HELP", "CommandFastPath", "CommandPlanner", "describe_step"]

HELP = (
    "I can look things up in the CRM.\n\n"
    "/leads [stage] — recent leads, optionally filtered\n"
    "   stages: nuevo, nutricion, en_proceso, cerrado, perdido\n"
    "/lead <id> — one lead in full\n"
    "/deals — purchase processes\n"
    "/search <text> — search leads, properties and deals\n"
    "/whoami — which tenant this conversation is bound to\n"
    "/debug — what the last answer cost, and on which model\n"
    "/help — this message\n\n"
    "Or just ask in your own words."
)

STAGES = {"nuevo", "nutricion", "en_proceso", "cerrado", "perdido"}

UNKNOWN = "I did not recognise that command. Send /help to see the list."


def _truncate(text: str, limit: int = 60) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


class CommandPlanner:
    """Maps one command to one tool call, then renders the result."""

    def __init__(self, namespace: str = "itmano_crm") -> None:
        self.namespace = namespace

    async def plan(self, request: PlanRequest) -> Plan:
        if request.iteration == 1:
            return self._dispatch(request)
        return Plan(reply=self._render(request))

    def _dispatch(self, request: PlanRequest) -> Plan:
        message = next(
            (turn.content for turn in reversed(request.history) if turn.role is Role.USER),
            "",
        ).strip()

        if not message.startswith("/"):
            return Plan(reply=UNKNOWN)

        head, _, tail = message.partition(" ")
        command = head.lstrip("/").split("@", 1)[0].lower()
        argument = tail.strip()

        match command:
            case "start" | "help":
                return Plan(reply=HELP)
            case "whoami":
                return self._call("whoami", {})
            case "deals":
                return self._call("list_deals", {"limit": 10})
            case "leads":
                if argument and argument not in STAGES:
                    return Plan(
                        reply=f"'{argument}' is not a stage. Try: {', '.join(sorted(STAGES))}."
                    )
                arguments: dict[str, Any] = {"limit": 10}
                if argument:
                    arguments["stage"] = argument
                return self._call("list_leads", arguments)
            case "lead":
                if not argument:
                    return Plan(reply="Which lead? Use /lead <id>.")
                return self._call("get_lead", {"id": argument})
            case "search":
                if not argument:
                    return Plan(reply="Search for what? Use /search <text>.")
                return self._call("search", {"q": argument, "limit": 10})
            case _:
                return Plan(reply=UNKNOWN)

    def _call(self, tool: str, arguments: dict[str, Any]) -> Plan:
        return Plan(
            tool_calls=(
                ToolCall(id=f"cmd-{tool}", name=f"{self.namespace}.{tool}", arguments=arguments),
            )
        )

    def _render(self, request: PlanRequest) -> str:
        """Turn the tool result at the end of the transcript into a reply."""
        last = next(
            (turn for turn in reversed(request.history) if turn.role is Role.TOOL),
            None,
        )
        if last is None or last.tool_name is None:
            return "Something went wrong: no tool answered."

        envelope = json.loads(last.content)
        if envelope.get("status") != "ok":
            error = envelope.get("error") or {}
            return self._explain(str(error.get("code", "unknown")))

        data = envelope.get("data")
        tool = last.tool_name.rsplit(".", 1)[-1]
        match tool:
            case "whoami":
                return self._whoami(data)
            case "list_leads":
                return self._leads(data)
            case "get_lead":
                return self._lead(data)
            case "list_deals":
                return self._deals(data)
            case "search":
                return self._search(data)
            case _:
                return json.dumps(data, ensure_ascii=False)[:800]

    @staticmethod
    def _explain(code: str) -> str:
        """Say what happened without repeating an upstream message verbatim."""
        match code:
            case "not_found":
                return "Nothing with that id."
            case "invalid_arguments":
                return "The CRM refused those arguments. Check /help."
            case "unauthorized":
                return "This connection is not allowed to do that."
            case "rate_limited":
                return "Too many requests just now. Try again in a moment."
            case "timeout":
                return "The CRM did not answer in time. Try again."
            case _:
                return "The CRM could not answer that right now."

    @staticmethod
    def _whoami(data: Any) -> str:
        tenant = data.get("tenant", {})
        return (
            f"Bound to {tenant.get('name', '?')} ({tenant.get('id', '?')})\n"
            f"environment: {data.get('environment', '?')}  "
            f"scopes: {', '.join(data.get('scopes', []))}"
        )

    @staticmethod
    def _leads(data: Any) -> str:
        rows = data.get("data", [])
        if not rows:
            return "No leads matched."
        lines = [
            f"• {row['id']}  {row.get('first_name', '')} {row.get('last_name') or ''}".rstrip()
            + f"  [{row.get('stage', '?')}]"
            for row in rows
        ]
        more = "\n\n(more pages available)" if data.get("next_cursor") else ""
        return f"{len(rows)} lead(s):\n" + "\n".join(lines) + more

    @staticmethod
    def _lead(data: Any) -> str:
        score = data.get("score") or {}
        budget = data.get("budget") or {}
        amount = f"{budget.get('amount')} {budget.get('currency')}" if budget else "not recorded"
        return (
            f"{data.get('first_name', '')} {data.get('last_name') or ''}".rstrip() + "\n"
            f"id: {data.get('id')}\n"
            f"stage: {data.get('stage', '?')}   quality: {data.get('quality_band') or '?'}\n"
            f"owner: {data.get('owner') or 'unassigned'}\n"
            f"email: {data.get('email', '?')}\n"
            f"phone: {data.get('phone') or 'none on file'}\n"
            f"budget: {amount}\n"
            f"score: {score.get('total', '?')}"
        )

    @staticmethod
    def _deals(data: Any) -> str:
        rows = data.get("data", [])
        if not rows:
            return "No purchase processes matched."
        lines = [
            f"• {_truncate(row.get('address') or 'no address')}"
            f"  closes {row.get('close_date') or 'no date set'}"
            f"  [{row.get('lead_stage', '?')}]"
            for row in rows
        ]
        # This CRM records no deal value. Saying so beats an absent field the
        # reader fills in with an assumption.
        return (
            f"{len(rows)} purchase process(es):\n"
            + "\n".join(lines)
            + "\n\n(no deal amounts are recorded in this CRM)"
        )

    @staticmethod
    def _search(data: Any) -> str:
        rows = data.get("data", [])
        if not rows:
            return "Nothing found."
        return f"{len(rows)} result(s):\n" + "\n".join(
            f"• [{row.get('type', '?')}] {row.get('label', '?')}  {row.get('id', '')}"
            for row in rows
        )


@dataclass(slots=True)
class CommandFastPath:
    """Commands answered deterministically; everything else goes to a model.

    Ownership of a turn is decided once, by the message that opened it: a slash
    command belongs to :class:`CommandPlanner` for both the dispatch and the
    rendering, anything else to ``fallback``. Deciding per iteration would let a
    turn change hands halfway through and render with the wrong formatter.

    This is also the safety net. If the model API is unreachable the commands
    keep working, so a demo does not go dark because someone else's service did.
    """

    fallback: Planner
    commands: CommandPlanner = field(default_factory=CommandPlanner)

    async def plan(self, request: PlanRequest) -> Plan:
        if self._is_command_turn(request):
            return await self.commands.plan(request)
        return await self.fallback.plan(request)

    @staticmethod
    def _is_command_turn(request: PlanRequest) -> bool:
        opening = next(
            (turn.content for turn in request.history if turn.role is Role.USER),
            "",
        )
        return opening.strip().startswith("/")


STEP_PHRASES: dict[str, str] = {
    "itmano_crm.list_leads": "Looking up leads",
    "itmano_crm.get_lead": "Fetching that lead",
    "itmano_crm.list_deals": "Looking up purchase processes",
    "itmano_crm.get_deal": "Fetching that purchase process",
    "itmano_crm.search": "Searching the CRM",
    "itmano_crm.metadata": "Checking what values this CRM accepts",
    "itmano_crm.whoami": "Checking which tenant I am bound to",
    "vibemarketolog.estimate_generation": "Pricing that, free of charge",
    "vibemarketolog.generate_image": "Generating the image",
}

SLOW_TOOLS: dict[str, str] = {
    "vibemarketolog.generate_image": "a minute or two",
}
"""Waits long enough that silence reads as a crash. Announce the duration
*before* it starts: an expected wait is patience, an unexplained one is a bug.

Deliberately a range rather than a number. Generation alone is ~80s for both
z-image and qwen-image-3, but a full turn measured 104s once the free price
checks and the two planner passes are counted. Promising "80 seconds" and taking
104 is worse than promising nothing: the person starts counting."""


def describe_step(call: ToolCall, spec: ToolSpec) -> str:
    """One line saying what the agent decided, before it acts on it.

    Shows the arguments too. A wrong filter is then visible at the moment it is
    chosen rather than inferred from a wrong answer two steps later.
    """
    phrase = STEP_PHRASES.get(call.name, f"Calling {call.name}")
    detail = ", ".join(
        f"{key}={value}"
        for key, value in sorted(call.arguments.items())
        if value is not None and key not in {"limit", "cursor", "prompt"}
    )
    line = f"{phrase}{f' ({detail})' if detail else ''}…"

    if spec.side_effect is SideEffect.WRITE:
        line += "\nThis one spends money."
    slow = SLOW_TOOLS.get(call.name)
    if slow:
        line += f" Takes {slow}."
    return line
