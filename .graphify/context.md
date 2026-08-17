# Graph Report - .  (2026-08-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 349 nodes · 1057 edges · 30 communities (22 shown, 8 thin omitted)
- Extraction: 67% EXTRACTED · 33% INFERRED · 0% AMBIGUOUS · INFERRED: 348 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9677d3fc`
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
- Community 20
- Community 21
- Community 22
- Community 23
- Community 24
- Community 25
- Community 26
- Community 27
- Community 28
- Community 29

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
- `RecordingAudit` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `ScriptedPlanner` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `TestTerminating` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `RecordingAudit` --uses--> `Turn`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `ScriptedPlanner` --uses--> `Turn`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py

## Import Cycles
- None detected.

## Communities (30 total, 8 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (34): DuplicateToolError, BaseModel, Protocol, Tool registry and calling protocol. This module is the contract every other…, The shape of a tool implementation., Raised when two tools claim the same name., Raised when a name is looked up that was never registered., Raised on an attempt to register after the registry was frozen. (+26 more)

### Community 1 - "Community 1"
Cohesion: 0.25
Nodes (27): AuditEvent, AuditPhase, NullAuditSink, PlanRequest, StrEnum, Orchestration loop: intent, plan, guard, execute, report. The loop owns the…, ``INTENT`` is written before the call runs, ``OUTCOME`` after., One record in the action log. Serialisable, no live objects. (+19 more)

### Community 2 - "Community 2"
Cohesion: 0.15
Nodes (10): Plan, Default guard until ``conduit.core.guard`` lands: reads pass, writes do not.…, What the planner returns. A plan with no tool calls ends the turn; ``reply`` is…, ReadOnlyGuard, Name-to-implementation map, populated at startup and then frozen. Freezing…, ToolRegistry, Emits a fixed sequence of plans, one per iteration., RecordingAudit (+2 more)

### Community 3 - "Community 3"
Cohesion: 0.14
Nodes (10): mock, parametrize, error_body(), Any, If this ever stops being null the tool description is a lie., What a challenge page or a proxy error actually looks like., The contract really does declare 201 here, not 200., TestErrorTranslation (+2 more)

### Community 4 - "Community 4"
Cohesion: 0.16
Nodes (14): BaseException, ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., Self, client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated() (+6 more)

### Community 5 - "Community 5"
Cohesion: 0.23
Nodes (16): CreateEmailDraftParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, ListDealsParams, NoParams (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.16
Nodes (8): LeadStage, Funnel stage. Moved by a person, never by the system., agent_tool_operations(), Operation ids the contract marks as belonging in an agent's catalogue.…, ToolRegistry, The planner sees descriptions and nothing else., TestContract, TestRegistration

### Community 7 - "Community 7"
Cohesion: 0.31
Nodes (5): A request to run one tool, as the planner emits it., Per-invocation identity and correlation. ``tenant_id`` is carried, never…, ToolCall, ToolContext, TestInvoke

### Community 8 - "Community 8"
Cohesion: 0.22
Nodes (10): fixture, ItmanoCrmSettings, ctx(), registry(), crm(), crm_registry(), ItmanoCrmClient, Offline tests for the CRM adapter. Every response here comes from… (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.23
Nodes (9): CrmError, _float_header(), _int_header(), Any, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift…, A call that did not succeed, already in CONDUIT's error vocabulary., Exception (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.24
Nodes (8): BaseSettings, CrmResponse, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, A successful call, plus the headers worth carrying forward., ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the…, Adapter for the ITMANO CRM agent surface (``/agent/v1``). The CRM owns tenant…

### Community 11 - "Community 11"
Cohesion: 0.27
Nodes (5): Agent, GuardDecision, Verdict on a single proposed call., Runs one user turn to completion. ``max_iterations`` bounds plan/execute…, Guard, audit the intent, run, audit the outcome. In that order.

### Community 12 - "Community 12"
Cohesion: 0.20
Nodes (6): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., Operation, One route, as the contract describes it., Client-side timeout: the server's deadline plus room to answer., RuntimeError

### Community 13 - "Community 13"
Cohesion: 0.24
Nodes (10): Any, ItmanoCrmClient, ToolRegistry, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register(), _run(), _spec() (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.25
Nodes (4): BaseModel, Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 15 - "Community 15"
Cohesion: 0.28
Nodes (7): contract_version(), load_contract(), operations(), Any, The published contract, vendored. ``contract/openapi.json`` is a byte-for-byte…, Parse the vendored document. Cached; the file cannot change at runtime., Every operation in the contract, keyed by ``operationId``.

### Community 16 - "Community 16"
Cohesion: 0.33
Nodes (4): CreateLeadParams, ListLeadsParams, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 17 - "Community 17"
Cohesion: 0.22
Nodes (7): AuditSink, Guard, Planner, Protocol, Turns a transcript plus a tool catalogue into the next step., Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation.

### Community 18 - "Community 18"
Cohesion: 0.29
Nodes (4): Any, Argument schema, in the form a function-calling planner expects., Every spec, or only those of one adapter, sorted by name., What the planner is shown.

### Community 19 - "Community 19"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 20 - "Community 20"
Cohesion: 0.33
Nodes (5): AgentReply, ExecutedCall, BaseModel, A call the loop actually considered, and what came of it., The outcome of one user turn.

### Community 22 - "Community 22"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 2` to `Community 0`, `Community 1`, `Community 7`, `Community 8`, `Community 11`, `Community 17`, `Community 18`, `Community 20`?**
  _High betweenness centrality (0.144) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 4` to `Community 9`, `Community 10`, `Community 12`, `Community 14`, `Community 15`, `Community 21`?**
  _High betweenness centrality (0.083) - this node is a cross-community bridge._
- **Why does `ToolContext` connect `Community 7` to `Community 0`, `Community 1`, `Community 2`, `Community 8`, `Community 11`, `Community 17`, `Community 20`?**
  _High betweenness centrality (0.079) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `ToolRegistry` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolRegistry` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ToolContext` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolContext` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolCall` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolCall` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolSpec` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolSpec` has 28 INFERRED edges - model-reasoned connections that need verification._