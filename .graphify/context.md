# Graph Report - .  (2026-08-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 355 nodes · 1068 edges · 20 communities (13 shown, 7 thin omitted)
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 348 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `97226ccb`
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
- `EchoParams` --uses--> `SideEffect`  [INFERRED]
  tests/conftest.py → conduit/core/tools.py
- `NoParams` --uses--> `SideEffect`  [INFERRED]
  tests/conftest.py → conduit/core/tools.py
- `TestInvoke` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py
- `TestRegistry` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py
- `TestResultEnvelope` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py

## Import Cycles
- None detected.

## Communities (20 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (56): Agent, AgentReply, AuditEvent, AuditPhase, AuditSink, ExecutedCall, Guard, GuardDecision (+48 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (49): AsyncClient, BaseException, BaseModel, BaseSettings, ConfigurationError, CrmError, CrmResponse, _float_header() (+41 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (38): DuplicateToolError, BaseModel, Protocol, Tool registry and calling protocol. This module is the contract every other…, The shape of a tool implementation., Raised when two tools claim the same name., Raised when a name is looked up that was never registered., Raised on an attempt to register after the registry was frozen. (+30 more)

### Community 3 - "Community 3"
Cohesion: 0.13
Nodes (12): LeadStage, Funnel stage. Moved by a person, never by the system., mock, parametrize, error_body(), Any, If this ever stops being null the tool description is a lie., What a challenge page or a proxy error actually looks like. (+4 more)

### Community 4 - "Community 4"
Cohesion: 0.23
Nodes (16): CreateEmailDraftParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, ListDealsParams, NoParams (+8 more)

### Community 5 - "Community 5"
Cohesion: 0.19
Nodes (9): Any, Argument schema, in the form a function-calling planner expects., Every spec, or only those of one adapter, sorted by name., What the planner is shown., main(), percentile(), Measure what a CRM tool call actually costs, through the real invocation path.…, timed() (+1 more)

### Community 6 - "Community 6"
Cohesion: 0.22
Nodes (10): fixture, ItmanoCrmSettings, ctx(), registry(), crm(), crm_registry(), ItmanoCrmClient, Offline tests for the CRM adapter. Every response here comes from… (+2 more)

### Community 7 - "Community 7"
Cohesion: 0.24
Nodes (10): Any, ItmanoCrmClient, ToolRegistry, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register(), _run(), _spec() (+2 more)

### Community 8 - "Community 8"
Cohesion: 0.33
Nodes (4): CreateLeadParams, ListLeadsParams, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 9 - "Community 9"
Cohesion: 0.38
Nodes (3): ToolRegistry, The planner sees descriptions and nothing else., TestRegistration

### Community 10 - "Community 10"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 11 - "Community 11"
Cohesion: 0.33
Nodes (3): agent_tool_operations(), Operation ids the contract marks as belonging in an agent's catalogue.…, TestContract

### Community 12 - "Community 12"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 2` to `Community 0`, `Community 5`, `Community 6`?**
  _High betweenness centrality (0.141) - this node is a cross-community bridge._
- **Why does `ToolContext` connect `Community 0` to `Community 2`, `Community 6`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `ToolRegistry` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolRegistry` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ToolContext` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolContext` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolCall` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolCall` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolSpec` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolSpec` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ToolResult` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolResult` has 30 INFERRED edges - model-reasoned connections that need verification._