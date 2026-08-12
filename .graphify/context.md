# Graph Report - .  (2026-08-12)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 186 nodes · 732 edges · 21 communities (14 shown, 7 thin omitted)
- Extraction: 57% EXTRACTED · 43% INFERRED · 0% AMBIGUOUS · INFERRED: 317 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d14ce5e1`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Community 0
- Community 1
- Community 2
- Community 3
- Community 4
- Community 5
- Community 6
- Community 7
- Community 8
- Community 9
- Community 10
- Community 11
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19
- Community 20
- Community 21

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 70 edges
2. `ToolContext` - 61 edges
3. `ToolCall` - 53 edges
4. `ToolSpec` - 46 edges
5. `ToolResult` - 44 edges
6. `SideEffect` - 39 edges
7. `ToolStatus` - 34 edges
8. `Plan` - 33 edges
9. `Agent` - 31 edges
10. `ScriptedPlanner` - 31 edges

## Surprising Connections (you probably didn't know these)
- `PermissiveGuard` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `RecordingAudit` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `ScriptedPlanner` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `TestAudit` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `TestExecution` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py

## Import Cycles
- None detected.

## Communities (21 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.13
Nodes (16): AgentReply, ExecutedCall, GuardDecision, NullAuditSink, BaseModel, Verdict on a single proposed call., Discards everything. Only acceptable in tests and phase-1 scaffolding., A call the loop actually considered, and what came of it. (+8 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (14): Any, AuditSink, Guard, Planner, Protocol, Turns a transcript plus a tool catalogue into the next step., Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation. (+6 more)

### Community 2 - "Community 2"
Cohesion: 0.12
Nodes (9): Protocol, The shape of a tool implementation., Name-to-implementation map, populated at startup and then frozen. Freezing…, Add a tool. Raises rather than silently replacing an existing name., Decorator form of :meth:`register`., RegisteredTool, ToolHandler, ToolRegistry (+1 more)

### Community 3 - "Community 3"
Cohesion: 0.30
Nodes (12): AuditPhase, PlanRequest, StrEnum, Orchestration loop: intent, plan, guard, execute, report. The loop owns the…, ``INTENT`` is written before the call runs, ``OUTCOME`` after., What the planner is given. Deliberately model-agnostic., Role, StopReason (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.27
Nodes (10): What a tool does to the world. The guard treats these very differently:…, SideEffect, fixture, ctx(), EchoParams, NoParams, BaseModel, Shared fixtures. Nothing here talks to a real system. (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.28
Nodes (8): Plan, Default guard until ``conduit.core.guard`` lands: reads pass, writes do not.…, What the planner returns. A plan with no tool calls ends the turn; ``reply`` is…, ReadOnlyGuard, Emits a fixed sequence of plans, one per iteration., ScriptedPlanner, TestAudit, TestGuardOrdering

### Community 6 - "Community 6"
Cohesion: 0.27
Nodes (6): Raised on an attempt to register after the registry was frozen., RegistryFrozenError, RuntimeError, _spec(), TestRegistry, TestSpec

### Community 7 - "Community 7"
Cohesion: 0.28
Nodes (5): BaseModel, Structured failure detail. Safe to serialise into the audit log., Uniform envelope returned by every tool. Handlers return this instead of…, ToolError, ToolResult

### Community 8 - "Community 8"
Cohesion: 0.25
Nodes (7): DuplicateToolError, StrEnum, Tool registry and calling protocol. This module is the contract every other…, Raised when two tools claim the same name., Provider-agnostic failure taxonomy. Adapters map their own upstream errors onto…, ToolErrorCode, ValueError

### Community 9 - "Community 9"
Cohesion: 0.48
Nodes (3): Agent, Runs one user turn to completion. ``max_iterations`` bounds plan/execute…, TestTerminating

### Community 10 - "Community 10"
Cohesion: 0.47
Nodes (4): One entry in the conversation transcript., Turn, PermissiveGuard, TestExecution

### Community 11 - "Community 11"
Cohesion: 0.50
Nodes (3): AuditEvent, One record in the action log. Serialisable, no live objects., RecordingAudit

### Community 14 - "Community 14"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

### Community 15 - "Community 15"
Cohesion: 0.67
Nodes (3): Raised when a name is looked up that was never registered., UnknownToolError, KeyError

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 2` to `Community 0`, `Community 1`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 13`?**
  _High betweenness centrality (0.218) - this node is a cross-community bridge._
- **Why does `ToolSpec` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 13`?**
  _High betweenness centrality (0.108) - this node is a cross-community bridge._
- **Why does `ToolContext` connect `Community 0` to `Community 1`, `Community 2`, `Community 3`, `Community 4`, `Community 5`, `Community 6`, `Community 8`, `Community 9`, `Community 10`, `Community 11`, `Community 13`?**
  _High betweenness centrality (0.099) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `ToolRegistry` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolRegistry` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ToolContext` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolContext` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolCall` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolCall` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolSpec` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolSpec` has 28 INFERRED edges - model-reasoned connections that need verification._