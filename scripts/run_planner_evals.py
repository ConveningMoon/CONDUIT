"""Run the planner golden set against one or more models.

Costs money. Prints the projected spend and refuses to start if it would take the
balance below the reserve kept for the live demo.

Measures four things per model: did it pick the right tool, did it pass the right
arguments, how often did the reply fail to parse, and how long did it take. Three
tries at one case is an impression; this is a number.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import statistics
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from conduit.adapters.itmano_crm import ItmanoCrmClient, ItmanoCrmSettings
from conduit.adapters.itmano_crm.tools import register
from conduit.adapters.vibemarketolog import (
    PLANNER_MODELS,
    LlmPlanner,
    VibemarketologClient,
    VibemarketologSettings,
)
from conduit.adapters.vibemarketolog import register as register_generation
from conduit.core.agent import PlanRequest, Role, Turn
from conduit.core.telemetry import turn_ledger
from conduit.core.tools import ToolRegistry, ToolSpec

EVALS = Path(__file__).resolve().parent.parent / "evals"
GOLDEN_SET = EVALS / "planner_golden_set.json"
HOLDOUT = EVALS / "planner_holdout.json"
DEMO_RESERVE_RUB = 250.0
"""Kept back for the live demo on the expensive model.

Sized, not guessed: a 30-minute conversation is 20-40 turns; at roughly 5.3₽ a
turn on the expensive model that is ~212₽, and 250₽ covers it with room for
retries on the day. Development spends what is above this line and nothing below.
"""


@dataclass(slots=True)
class Outcome:
    case_id: str
    chose: str | None
    expected: str | None
    tool_ok: bool
    arguments_ok: bool
    parse_failed: bool
    latency_ms: int
    cost_rub: float
    retries: int
    detail: str = ""


@dataclass(slots=True)
class Report:
    model: str
    outcomes: list[Outcome] = field(default_factory=list)

    @property
    def tool_accuracy(self) -> float:
        return sum(o.tool_ok for o in self.outcomes) / max(len(self.outcomes), 1)

    @property
    def argument_accuracy(self) -> float:
        graded = [o for o in self.outcomes if o.expected is not None]
        return sum(o.arguments_ok for o in graded) / max(len(graded), 1)

    @property
    def parse_failure_rate(self) -> float:
        return sum(o.parse_failed for o in self.outcomes) / max(len(self.outcomes), 1)

    @property
    def total_cost(self) -> float:
        return sum(o.cost_rub for o in self.outcomes)


def normalise(spec: ToolSpec | None, arguments: dict[str, Any]) -> dict[str, Any]:
    """Put the planner's arguments through the tool's own validation first.

    What matters is whether the call would work, not whether the raw string
    matched. The CRM adapter accepts documented English aliases for its Spanish
    enums, so a planner answering "nurturing" produces a perfectly good call —
    grading the raw text scores that as a miss and understates the model.
    """
    if spec is None:
        return arguments
    try:
        return dict(spec.params.model_validate(arguments).model_dump(mode="json"))
    except Exception:
        return arguments


def grade(
    case: dict[str, Any], chose: str | None, arguments: dict[str, Any]
) -> tuple[bool, bool, str]:
    expected = case.get("expected_tool")
    acceptable = set(case.get("acceptable_tools") or [])

    if expected is None:
        # The honest answer is no tool at all; a listed alternative is tolerable.
        ok = chose is None or chose in acceptable
        return ok, ok, "" if ok else f"reached for {chose} instead of refusing"

    if chose != expected and chose not in acceptable:
        return False, False, f"chose {chose or 'nothing'}"

    missing: list[str] = []
    for key, want in (case.get("expected_arguments") or {}).items():
        got = arguments.get(key)
        if isinstance(want, str) and isinstance(got, str):
            if want.casefold() not in got.casefold() and got.casefold() not in want.casefold():
                missing.append(f"{key}={got!r} (wanted {want!r})")
        elif got != want:
            missing.append(f"{key}={got!r} (wanted {want!r})")

    return True, not missing, "; ".join(missing)


async def run_model(
    model: str,
    cases: list[dict[str, Any]],
    specs: tuple[ToolSpec, ...],
    names: frozenset[str],
) -> Report:
    report = Report(model=model)
    settings = VibemarketologSettings()

    async with VibemarketologClient(settings) as client:
        planner = LlmPlanner(client=client, model=model, known_tools=names)
        for case in cases:
            request = PlanRequest(
                history=(Turn(role=Role.USER, content=case["message"]),),
                tools=specs,
                iteration=1,
            )
            with turn_ledger() as ledger:
                plan = await planner.plan(request)

            chose = plan.tool_calls[0].name if plan.tool_calls else None
            raw = dict(plan.tool_calls[0].arguments) if plan.tool_calls else {}
            spec = next((s for s in specs if s.name == chose), None)
            tool_ok, arguments_ok, detail = grade(case, chose, normalise(spec, raw))
            retries = sum(1 for entry in ledger if entry.retry)

            report.outcomes.append(
                Outcome(
                    case_id=case["id"],
                    chose=chose,
                    expected=case.get("expected_tool"),
                    tool_ok=tool_ok,
                    arguments_ok=arguments_ok,
                    parse_failed=retries > 0,
                    latency_ms=sum(entry.latency_ms for entry in ledger),
                    cost_rub=sum(entry.cost_rub for entry in ledger),
                    retries=retries,
                    detail=detail,
                )
            )
    return report


def print_report(report: Report) -> None:
    print(f"\n===== {report.model} =====")
    print(f"| {'case':28} | {'tool':5} | {'args':5} | {'ms':>6} | detail")
    print(f"| {'-' * 28} | {'-' * 5} | {'-' * 5} | {'-' * 6} | ------")
    for o in report.outcomes:
        print(
            f"| {o.case_id:28} | {'ok' if o.tool_ok else 'FAIL':5} "
            f"| {'ok' if o.arguments_ok else 'FAIL':5} | {o.latency_ms:6} | {o.detail}"
        )
    latencies = [o.latency_ms for o in report.outcomes]
    print(
        f"\n  tool accuracy      {report.tool_accuracy:.0%}"
        f"\n  argument accuracy  {report.argument_accuracy:.0%}"
        f"\n  parse failures     {report.parse_failure_rate:.0%}"
        f"\n  latency p50/max    {statistics.median(latencies):.0f}ms / {max(latencies)}ms"
        f"\n  spend              {report.total_cost:.2f} ₽"
    )


async def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=["gpt-5.6-luna"])
    parser.add_argument(
        "--holdout",
        action="store_true",
        help="run the held-out cases instead of the tuning set",
    )
    parser.add_argument("--yes", action="store_true", help="skip the spend confirmation")
    args = parser.parse_args()

    source = HOLDOUT if args.holdout else GOLDEN_SET
    document = json.loads(source.read_text(encoding="utf-8"))
    print(f"set: {source.name}")
    cases = document["cases"]

    projected = sum(PLANNER_MODELS.get(m, 4.0) * len(cases) for m in args.models)
    async with VibemarketologClient(VibemarketologSettings()) as probe:
        balance = await probe.balance_rub()

    print(f"balance {balance:.2f} RUB · {len(cases)} cases, {len(args.models)} model(s)")
    print(f"projected spend {projected:.2f} ₽ · leaves {balance - projected:.2f} ₽")
    if balance - projected < DEMO_RESERVE_RUB:
        print(
            f"REFUSING: that would break the {DEMO_RESERVE_RUB:.0f} ₽ reserve held for the demo.",
            file=sys.stderr,
        )
        return 1
    if not args.yes:
        print("pass --yes to spend it")
        return 0

    crm = ItmanoCrmClient(ItmanoCrmSettings())
    platform = VibemarketologClient(VibemarketologSettings())
    try:
        await crm.verify()
        registry = ToolRegistry()
        register(registry, crm)
        # Both adapters, or a case about generating an image measures nothing but
        # the absence of the tool.
        register_generation(registry, platform)
        registry.freeze()
        specs = tuple(registry.specs())
        names = frozenset(spec.name for spec in specs)

        for model in args.models:
            print_report(await run_model(model, cases, specs, names))
    finally:
        await crm.aclose()
        await platform.aclose()

    async with VibemarketologClient(VibemarketologSettings()) as probe:
        print(f"\nbalance after: {await probe.balance_rub():.2f} ₽")
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
