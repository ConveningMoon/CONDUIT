# Graph Report - .  (2026-08-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 265 nodes · 879 edges · 20 communities (13 shown, 7 thin omitted)
- Extraction: 63% EXTRACTED · 37% INFERRED · 0% AMBIGUOUS · INFERRED: 327 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `6b0c1cbd`
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
- Community 12
- Community 13
- Community 14
- Community 15
- Community 16
- Community 17
- Community 18
- Community 19

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
- `ExplodingPlanner` --uses--> `GuardDecision`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `PermissiveGuard` --uses--> `GuardDecision`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `RecordingAudit` --uses--> `GuardDecision`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `ScriptedPlanner` --uses--> `GuardDecision`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `TestAudit` --uses--> `GuardDecision`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py

## Import Cycles
- None detected.

## Communities (20 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.16
Nodes (36): Agent, AuditEvent, AuditPhase, Plan, PlanRequest, BaseModel, StrEnum, Orchestration loop: intent, plan, guard, execute, report. The loop owns the… (+28 more)

### Community 1 - "Community 1"
Cohesion: 0.07
Nodes (34): DuplicateToolError, Protocol, Tool registry and calling protocol. This module is the contract every other…, The shape of a tool implementation., Raised when two tools claim the same name., Raised when a name is looked up that was never registered., Raised on an attempt to register after the registry was frozen., Name-to-implementation map, populated at startup and then frozen. Freezing… (+26 more)

### Community 2 - "Community 2"
Cohesion: 0.13
Nodes (17): AgentReply, ExecutedCall, Guard, GuardDecision, NullAuditSink, Verdict on a single proposed call., Deterministic-first gate in front of every call. Implementations run cheap…, Discards everything. Only acceptable in tests and phase-1 scaffolding. (+9 more)

### Community 3 - "Community 3"
Cohesion: 0.11
Nodes (12): Any, AuditSink, Planner, Protocol, Turns a transcript plus a tool catalogue into the next step., Where action records go. The hash chain lives in the implementation., Everything the rest of the system needs to know about a tool. Declared once by…, Adapter this tool belongs to, e.g. ``itmano_crm``. (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (14): BaseException, ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., Self, client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated() (+6 more)

### Community 5 - "Community 5"
Cohesion: 0.21
Nodes (10): CrmError, _float_header(), _int_header(), Any, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift…, A call that did not succeed, already in CONDUIT's error vocabulary. (+2 more)

### Community 6 - "Community 6"
Cohesion: 0.20
Nodes (6): BaseModel, ConfigurationError, Refuse to serve anything if the server is not who we expect. Called once before…, The adapter is pointed somewhere it was not meant to reach., Identity the server reports for our token., WhoAmI

### Community 7 - "Community 7"
Cohesion: 0.24
Nodes (7): BaseSettings, CrmResponse, A successful call, plus the headers worth carrying forward., ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the…, Adapter for the ITMANO CRM agent surface (``/agent/v1``). The CRM owns tenant…

### Community 8 - "Community 8"
Cohesion: 0.28
Nodes (7): contract_version(), load_contract(), operations(), Any, The published contract, vendored. ``contract/openapi.json`` is a byte-for-byte…, Parse the vendored document. Cached; the file cannot change at runtime., Every operation in the contract, keyed by ``operationId``.

### Community 9 - "Community 9"
Cohesion: 0.33
Nodes (3): Operation, One route, as the contract describes it., Client-side timeout: the server's deadline plus room to answer.

### Community 10 - "Community 10"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 11 - "Community 11"
Cohesion: 0.33
Nodes (3): BaseModel, Structured failure detail. Safe to serialise into the audit log., ToolError

### Community 13 - "Community 13"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 1` to `Community 0`, `Community 2`, `Community 3`?**
  _High betweenness centrality (0.175) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 4` to `Community 5`, `Community 6`, `Community 7`, `Community 8`, `Community 9`, `Community 12`?**
  _High betweenness centrality (0.105) - this node is a cross-community bridge._
- **Why does `ToolSpec` connect `Community 3` to `Community 0`, `Community 1`, `Community 2`, `Community 11`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `ToolRegistry` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolRegistry` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ToolContext` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolContext` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolCall` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolCall` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolSpec` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolSpec` has 28 INFERRED edges - model-reasoned connections that need verification._