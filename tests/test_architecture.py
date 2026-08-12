"""Executable form of the dependency rule: the core points inward only."""

from __future__ import annotations

import ast
from pathlib import Path

CORE = Path(__file__).resolve().parent.parent / "conduit" / "core"
FORBIDDEN_PREFIXES = ("conduit.adapters", "conduit.interfaces", "conduit.demo_data")


def _imported_modules(source: str) -> list[str]:
    tree = ast.parse(source)
    modules: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module is not None and node.level == 0:
            modules.append(node.module)
    return modules


def test_core_never_imports_adapters_or_interfaces() -> None:
    offenders: list[str] = []
    for path in CORE.rglob("*.py"):
        for module in _imported_modules(path.read_text(encoding="utf-8")):
            if module.startswith(FORBIDDEN_PREFIXES):
                offenders.append(f"{path.name} imports {module}")
    assert not offenders, "core must not depend outward: " + "; ".join(offenders)
