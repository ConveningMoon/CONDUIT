# Graph Report - .  (2026-08-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 635 nodes · 1694 edges · 35 communities (19 shown, 16 thin omitted)
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 380 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `66abe309`
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
- Community 30
- Community 31
- Community 32
- Community 33
- Community 34

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 70 edges
2. `ToolContext` - 61 edges
3. `ToolCall` - 53 edges
4. `ToolSpec` - 46 edges
5. `ToolResult` - 44 edges
6. `InMemoryGuardStore` - 40 edges
7. `SideEffect` - 39 edges
8. `DeterministicGuard` - 37 edges
9. `ToolStatus` - 34 edges
10. `Plan` - 33 edges

## Surprising Connections (you probably didn't know these)
- `EchoParams` --uses--> `SideEffect`  [INFERRED]
  tests/conftest.py → conduit/core/tools.py
- `TestRegistry` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py
- `TestResultEnvelope` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py
- `TestSpec` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py
- `TestRegistry` --uses--> `ToolStatus`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py

## Import Cycles
- None detected.

## Communities (35 total, 16 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (66): Agent, AgentReply, AuditEvent, AuditPhase, AuditSink, ExecutedCall, Guard, GuardDecision (+58 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (43): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+35 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (45): Agent, Binding, BindingError, BindingTable, DenialReason, load_bindings(), Path, Which conversation may act for which tenant. This module is the authorization… (+37 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (28): ItmanoCrmClient, ItmanoCrmSettings, mock, main(), percentile(), Measure what a CRM tool call actually costs, through the real invocation path.…, timed(), crm() (+20 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (32): DuplicateToolError, Protocol, Tool registry and calling protocol. This module is the contract every other…, The shape of a tool implementation., Raised when two tools claim the same name., Raised when a name is looked up that was never registered., Raised on an attempt to register after the registry was frozen., Add a tool. Raises rather than silently replacing an existing name. (+24 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (25): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+17 more)

### Community 6 - "Community 6"
Cohesion: 0.11
Nodes (32): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+24 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 8 - "Community 8"
Cohesion: 0.16
Nodes (10): Any, Argument schema, in the form a function-calling planner expects., What the planner is shown., CommandPlanner, Plan, PlanRequest, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim. (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.19
Nodes (7): Plan, PlanRequest, Telegram sends /leads@thebot in groups., Plain text, no parse mode. The demo tenant seeds exactly this case., A missing number is a number the reader invents., TestCommandPlanner, TestRendering

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (14): BaseException, ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., Self, client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated() (+6 more)

### Community 11 - "Community 11"
Cohesion: 0.23
Nodes (9): CrmError, _float_header(), _int_header(), Any, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift…, A call that did not succeed, already in CONDUIT's error vocabulary., Exception (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.24
Nodes (8): BaseSettings, CrmResponse, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, A successful call, plus the headers worth carrying forward., ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the…, Adapter for the ITMANO CRM agent surface (``/agent/v1``). The CRM owns tenant…

### Community 13 - "Community 13"
Cohesion: 0.20
Nodes (6): GuardStore, Protocol, Record a write and return how many happened in the trailing hour., Record an intent and return how often it occurred inside the window., Counters and switches the rules read and write. Deliberately narrow, and every…, Record a call in this turn and return the running count, this one included.

### Community 14 - "Community 14"
Cohesion: 0.25
Nodes (4): BaseModel, Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 15 - "Community 15"
Cohesion: 0.22
Nodes (6): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., Operation, One route, as the contract describes it., Client-side timeout: the server's deadline plus room to answer., RuntimeError

### Community 16 - "Community 16"
Cohesion: 0.28
Nodes (7): contract_version(), load_contract(), operations(), Any, The published contract, vendored. ``contract/openapi.json`` is a byte-for-byte…, Parse the vendored document. Cached; the file cannot change at runtime., Every operation in the contract, keyed by ``operationId``.

### Community 17 - "Community 17"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 19 - "Community 19"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 0` to `Community 8`, `Community 4`?**
  _High betweenness centrality (0.078) - this node is a cross-community bridge._
- **Why does `InMemoryGuardStore` connect `Community 1` to `Community 5`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 10` to `Community 11`, `Community 12`, `Community 14`, `Community 15`, `Community 16`, `Community 18`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `ToolRegistry` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolRegistry` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ToolContext` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolContext` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolCall` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolCall` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolSpec` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolSpec` has 28 INFERRED edges - model-reasoned connections that need verification._