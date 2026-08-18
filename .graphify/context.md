# Graph Report - .  (2026-08-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 864 nodes · 2132 edges · 59 communities (30 shown, 29 thin omitted)
- Extraction: 81% EXTRACTED · 19% INFERRED · 0% AMBIGUOUS · INFERRED: 407 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `cb5ade0c`
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
- Community 53
- Community 54
- Community 55
- Community 56
- Community 57
- Community 58

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 53 edges
2. `PlanRequest` - 45 edges
3. `Plan` - 42 edges
4. `InMemoryGuardStore` - 40 edges
5. `ToolContext` - 39 edges
6. `Agent` - 38 edges
7. `DeterministicGuard` - 37 edges
8. `Turn` - 34 edges
9. `CommandPlanner` - 34 edges
10. `ToolCall` - 32 edges

## Surprising Connections (you probably didn't know these)
- `ExplodingPlanner` --uses--> `SideEffect`  [INFERRED]
  tests/test_agent.py → conduit/core/tools.py
- `PermissiveGuard` --uses--> `SideEffect`  [INFERRED]
  tests/test_agent.py → conduit/core/tools.py
- `RecordingAudit` --uses--> `SideEffect`  [INFERRED]
  tests/test_agent.py → conduit/core/tools.py
- `ScriptedPlanner` --uses--> `SideEffect`  [INFERRED]
  tests/test_agent.py → conduit/core/tools.py
- `TestAudit` --uses--> `SideEffect`  [INFERRED]
  tests/test_agent.py → conduit/core/tools.py

## Import Cycles
- None detected.

## Communities (59 total, 29 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (40): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+32 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (48): BaseModel, ConfigurationError, CrmError, CrmResponse, _float_header(), _int_header(), ItmanoCrmClient, Any (+40 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (47): Notified of each call the guard has allowed, just before it runs. The point is…, StepReporter, Which conversation may act for which tenant. This module is the authorization…, build_dispatcher(), BindingTable, Message, Telegram surface: resolve the conversation, then hand off to the agent. Replies…, Send one line per allowed call, before it runs. (+39 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (37): AsyncClient, BaseException, BaseSettings, Completion, GenerationError, _has_result(), Any, Client for the platform's text generation endpoint. ``type=text`` is… (+29 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (37): EstimateParams, _first_url(), GenerateImageParams, _Params, Any, BaseModel, ToolRegistry, VibemarketologClient (+29 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (31): PlanRequest, What the planner is given. Deliberately model-agnostic., Role, CommandFastPath, Commands answered deterministically; everything else goes to a model. Ownership…, LlmPlanner, completion(), parse() (+23 more)

### Community 6 - "Community 6"
Cohesion: 0.10
Nodes (28): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+20 more)

### Community 7 - "Community 7"
Cohesion: 0.17
Nodes (26): Agent, AuditEvent, AuditPhase, Plan, Orchestration loop: intent, plan, guard, execute, report. The loop owns the…, Default guard until ``conduit.core.guard`` lands: reads pass, writes do not.…, ``INTENT`` is written before the call runs, ``OUTCOME`` after., One record in the action log. Serialisable, no live objects. (+18 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (27): DuplicateToolError, BaseModel, StrEnum, Tool registry and calling protocol. This module is the contract every other…, Raised when two tools claim the same name., Raised when a name is looked up that was never registered., Raised on an attempt to register after the registry was frozen., What a tool does to the world. The guard treats these very differently:… (+19 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (12): CommandPlanner, Any, ToolCall, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim., Maps one command to one tool call, then renders the result., _truncate(), Telegram sends /leads@thebot in groups. (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.14
Nodes (13): AgentReply, ExecutedCall, GuardDecision, NullAuditSink, BaseModel, ToolCall, ToolContext, ToolSpec (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.11
Nodes (14): Binding, BindingError, BindingTable, DenialReason, load_bindings(), Path, Decide whether this message may act, and for whom., Read the binding file. Any doubt is fatal rather than permissive. (+6 more)

### Community 13 - "Community 13"
Cohesion: 0.13
Nodes (17): current_ledger(), ModelCall, Per-turn ledger of model calls. Cost and model choice are decisions this system…, One request to a language model, and what it cost., Collect every model call made inside this block., Add to the ledger if one is open. A no-op otherwise, never an error., record_model_call(), turn_ledger() (+9 more)

### Community 14 - "Community 14"
Cohesion: 0.18
Nodes (16): CreateEmailDraftParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, NoParams, _normalise_stage() (+8 more)

### Community 15 - "Community 15"
Cohesion: 0.17
Nodes (6): Name-to-implementation map, populated at startup and then frozen. Freezing…, ToolRegistry, fixture, ctx(), registry(), TestRegistry

### Community 16 - "Community 16"
Cohesion: 0.20
Nodes (8): CreateLeadParams, ListLeadsParams, won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestArgumentValidation, TestStageAliases

### Community 17 - "Community 17"
Cohesion: 0.21
Nodes (7): ListDealsParams, UpdateLeadParams, mock, If this ever stops being null the tool description is a lie., The contract really does declare 201 here, not 200., TestReadPaths, TestWritePaths

### Community 18 - "Community 18"
Cohesion: 0.21
Nodes (10): Any, ToolSpec, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register(), _run(), _spec(), ItmanoCrmClient (+2 more)

### Community 19 - "Community 19"
Cohesion: 0.32
Nodes (6): A request to run one tool, as the planner emits it., Per-invocation identity and correlation. ``tenant_id`` is carried, never…, Validate, run and time one call. Never raises. Anything a handler throws…, ToolCall, ToolContext, TestInvoke

### Community 20 - "Community 20"
Cohesion: 0.20
Nodes (7): LeadStage, Funnel stage. Moved by a person, never by the system., parametrize, error_body(), Any, What a challenge page or a proxy error actually looks like., TestErrorTranslation

### Community 21 - "Community 21"
Cohesion: 0.22
Nodes (4): The planner sees descriptions and nothing else., TestContract, TestRegistration, ToolRegistry

### Community 22 - "Community 22"
Cohesion: 0.27
Nodes (7): Any, Argument schema, in the form a function-calling planner expects., What the planner is shown., main(), percentile(), Measure what a CRM tool call actually costs, through the real invocation path.…, timed()

### Community 23 - "Community 23"
Cohesion: 0.20
Nodes (6): GuardStore, Protocol, Record a write and return how many happened in the trailing hour., Record an intent and return how often it occurred inside the window., Counters and switches the rules read and write. Deliberately narrow, and every…, Record a call in this turn and return the running count, this one included.

### Community 24 - "Community 24"
Cohesion: 0.24
Nodes (7): Protocol, The shape of a tool implementation., Add a tool. Raises rather than silently replacing an existing name., Decorator form of :meth:`register`., RegisteredTool, ToolHandler, P

### Community 25 - "Community 25"
Cohesion: 0.22
Nodes (7): AuditSink, Guard, Planner, Turns a transcript plus a tool catalogue into the next step., Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation., Protocol

### Community 26 - "Community 26"
Cohesion: 0.33
Nodes (4): Everything the rest of the system needs to know about a tool. Declared once by…, Adapter this tool belongs to, e.g. ``itmano_crm``., Every spec, or only those of one adapter, sorted by name., ToolSpec

### Community 27 - "Community 27"
Cohesion: 0.43
Nodes (6): ItmanoCrmSettings, crm(), crm_registry(), fixture, Offline tests for the CRM adapter. Every response here comes from…, settings()

### Community 28 - "Community 28"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 29 - "Community 29"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **29 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 15` to `Community 7`, `Community 8`, `Community 19`, `Community 22`, `Community 24`, `Community 26`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `PlanRequest` connect `Community 5` to `Community 2`, `Community 7`, `Community 9`, `Community 11`, `Community 12`, `Community 25`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `InMemoryGuardStore` connect `Community 0` to `Community 6`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ToolRegistry` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolRegistry` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `PlanRequest` (e.g. with `CommandFastPath` and `CommandPlanner`) actually correct?**
  _`PlanRequest` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Plan` (e.g. with `CommandFastPath` and `CommandPlanner`) actually correct?**
  _`Plan` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `InMemoryGuardStore` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`InMemoryGuardStore` has 10 INFERRED edges - model-reasoned connections that need verification._