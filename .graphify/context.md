# Graph Report - .  (2026-08-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 768 nodes · 1972 edges · 46 communities (22 shown, 24 thin omitted)
- Extraction: 78% EXTRACTED · 22% INFERRED · 0% AMBIGUOUS · INFERRED: 434 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3b2545f5`
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
- `TestChaining` --uses--> `GuardSettings`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestTampering` --uses--> `GuardSettings`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestThroughTheLoop` --uses--> `GuardSettings`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestChaining` --uses--> `InMemoryGuardStore`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestTampering` --uses--> `InMemoryGuardStore`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py

## Import Cycles
- None detected.

## Communities (46 total, 24 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (89): Agent, AgentReply, AuditEvent, AuditPhase, AuditSink, ExecutedCall, Guard, GuardDecision (+81 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (40): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+32 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (46): BaseModel, ConfigurationError, CrmError, CrmResponse, _float_header(), _int_header(), ItmanoCrmClient, Any (+38 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (40): build_system_prompt(), _clip(), LlmPlanner, _PlannedCall, _PlannerOutput, BaseModel, PlanRequest, A planner built on a text model that has no native function calling. The… (+32 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (30): CommandFastPath, CommandPlanner, Any, A deterministic planner for explicit commands. CONDUIT's orchestration loop…, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim., Commands answered deterministically; everything else goes to a model. Ownership…, Maps one command to one tool call, then renders the result. (+22 more)

### Community 5 - "Community 5"
Cohesion: 0.06
Nodes (36): Agent, BaseSettings, BindingTable, Binding, BindingError, BindingTable, DenialReason, load_bindings() (+28 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (28): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (21): AsyncClient, BaseException, Completion, GenerationError, Client for the platform's text generation endpoint. ``type=text`` is…, The platform did not return a usable completion., One synchronous text generation, recorded in the turn ledger., VibemarketologClient (+13 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (9): error_body(), Any, mock, If this ever stops being null the tool description is a lie., What a challenge page or a proxy error actually looks like., The contract really does declare 201 here, not 200., TestErrorTranslation, TestReadPaths (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.18
Nodes (16): CreateEmailDraftParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, NoParams, _normalise_stage() (+8 more)

### Community 11 - "Community 11"
Cohesion: 0.16
Nodes (13): agent_tool_operations(), Any, ToolSpec, Registration of the CRM tools into a :class:`ToolRegistry`. Descriptions here…, Operation ids the contract marks as belonging in an agent's catalogue.…, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register() (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.17
Nodes (9): LeadStage, ListDealsParams, Funnel stage. Moved by a person, never by the system., UpdateLeadParams, parametrize, A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestContract (+1 more)

### Community 13 - "Community 13"
Cohesion: 0.24
Nodes (8): grade(), main(), Outcome, print_report(), Any, Run the planner golden set against one or more models. Costs money. Prints the…, Report, run_model()

### Community 14 - "Community 14"
Cohesion: 0.25
Nodes (5): CreateLeadParams, ListLeadsParams, won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

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
Cohesion: 0.43
Nodes (6): ItmanoCrmSettings, crm(), crm_registry(), fixture, Offline tests for the CRM adapter. Every response here comes from…, settings()

### Community 19 - "Community 19"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 20 - "Community 20"
Cohesion: 0.50
Nodes (3): Any, Argument schema, in the form a function-calling planner expects., What the planner is shown.

### Community 21 - "Community 21"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **24 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 0` to `Community 17`, `Community 20`?**
  _High betweenness centrality (0.063) - this node is a cross-community bridge._
- **Why does `InMemoryGuardStore` connect `Community 1` to `Community 6`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 2` to `Community 7`?**
  _High betweenness centrality (0.035) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `ToolRegistry` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolRegistry` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ToolContext` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolContext` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolCall` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolCall` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolSpec` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolSpec` has 28 INFERRED edges - model-reasoned connections that need verification._