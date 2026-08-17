# Graph Report - .  (2026-08-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 745 nodes · 1908 edges · 53 communities (25 shown, 28 thin omitted)
- Extraction: 79% EXTRACTED · 21% INFERRED · 0% AMBIGUOUS · INFERRED: 397 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f0ddd7fb`
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
- Community 35
- Community 36
- Community 37
- Community 38
- Community 39
- Community 40
- Community 41
- Community 42
- Community 43
- Community 44
- Community 45
- Community 46
- Community 47
- Community 48
- Community 49
- Community 50
- Community 51
- Community 52

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
- `TestThroughTheLoop` --uses--> `AuditRecord`  [INFERRED]
  tests/test_audit.py → conduit/core/audit.py
- `TestThroughTheLoop` --uses--> `InMemoryAuditStore`  [INFERRED]
  tests/test_audit.py → conduit/core/audit.py
- `TestThroughTheLoop` --uses--> `HashChainAuditSink`  [INFERRED]
  tests/test_audit.py → conduit/core/audit.py
- `TestChaining` --uses--> `GuardSettings`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestTampering` --uses--> `GuardSettings`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py

## Import Cycles
- None detected.

## Communities (53 total, 28 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (86): Agent, AgentReply, AuditEvent, AuditPhase, AuditSink, ExecutedCall, Guard, GuardDecision (+78 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (54): AsyncClient, BaseModel, Completion, GenerationError, Client for the platform's text generation endpoint. ``type=text`` is…, The platform did not return a usable completion., One synchronous text generation, recorded in the turn ledger., VibemarketologClient (+46 more)

### Community 2 - "Community 2"
Cohesion: 0.08
Nodes (43): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+35 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (29): CommandFastPath, CommandPlanner, Any, A deterministic planner for explicit commands. CONDUIT's orchestration loop…, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim., Commands answered deterministically; everything else goes to a model. Ownership…, Maps one command to one tool call, then renders the result. (+21 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (37): Agent, BaseSettings, BindingTable, Binding, BindingError, BindingTable, DenialReason, load_bindings() (+29 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (25): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+17 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 7 - "Community 7"
Cohesion: 0.17
Nodes (19): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+11 more)

### Community 8 - "Community 8"
Cohesion: 0.16
Nodes (10): CrmError, _float_header(), _int_header(), Any, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift…, A call that did not succeed, already in CONDUIT's error vocabulary., Exception (+2 more)

### Community 9 - "Community 9"
Cohesion: 0.22
Nodes (9): grade(), main(), Outcome, print_report(), Any, Run the planner golden set against one or more models. Costs money. Prints the…, Report, run_model() (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.23
Nodes (5): parse(), Models wrap JSON in fences constantly, whatever the instructions say., Code catches this, not the model's good behaviour., A model adding commentary keys should not fail the whole plan., TestParsing

### Community 11 - "Community 11"
Cohesion: 0.23
Nodes (9): ConfigurationError, CrmResponse, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, The adapter is pointed somewhere it was not meant to reach., A successful call, plus the headers worth carrying forward., ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the… (+1 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (10): contract_version(), load_contract(), operations(), Any, The published contract, vendored. ``contract/openapi.json`` is a byte-for-byte…, Parse the vendored document. Cached; the file cannot change at runtime., Every operation in the contract, keyed by ``operationId``., agent_tool_operations() (+2 more)

### Community 13 - "Community 13"
Cohesion: 0.21
Nodes (10): Any, ToolSpec, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register(), _run(), _spec(), ItmanoCrmClient (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.27
Nodes (11): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated(), test_an_unknown_lead_maps_to_not_found(), test_identity_matches_what_we_expect() (+3 more)

### Community 15 - "Community 15"
Cohesion: 0.27
Nodes (7): main(), percentile(), Measure what a CRM tool call actually costs, through the real invocation path.…, timed(), The planner sees descriptions and nothing else., TestRegistration, ToolRegistry

### Community 16 - "Community 16"
Cohesion: 0.20
Nodes (6): GuardStore, Protocol, Record a write and return how many happened in the trailing hour., Record an intent and return how often it occurred inside the window., Counters and switches the rules read and write. Deliberately narrow, and every…, Record a call in this turn and return the running count, this one included.

### Community 17 - "Community 17"
Cohesion: 0.24
Nodes (7): Protocol, The shape of a tool implementation., Add a tool. Raises rather than silently replacing an existing name., Decorator form of :meth:`register`., RegisteredTool, ToolHandler, P

### Community 18 - "Community 18"
Cohesion: 0.29
Nodes (3): Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 19 - "Community 19"
Cohesion: 0.29
Nodes (4): error_body(), parametrize, What a challenge page or a proxy error actually looks like., TestErrorTranslation

### Community 20 - "Community 20"
Cohesion: 0.43
Nodes (6): ItmanoCrmSettings, crm(), crm_registry(), fixture, Offline tests for the CRM adapter. Every response here comes from…, settings()

### Community 23 - "Community 23"
Cohesion: 0.33
Nodes (3): Operation, One route, as the contract describes it., Client-side timeout: the server's deadline plus room to answer.

### Community 24 - "Community 24"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 25 - "Community 25"
Cohesion: 0.50
Nodes (3): Any, Argument schema, in the form a function-calling planner expects., What the planner is shown.

### Community 27 - "Community 27"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **28 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 0` to `Community 25`, `Community 17`, `Community 1`?**
  _High betweenness centrality (0.064) - this node is a cross-community bridge._
- **Why does `InMemoryGuardStore` connect `Community 2` to `Community 5`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `CommandPlanner` connect `Community 3` to `Community 4`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `ToolRegistry` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolRegistry` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ToolContext` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolContext` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolCall` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolCall` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolSpec` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolSpec` has 28 INFERRED edges - model-reasoned connections that need verification._