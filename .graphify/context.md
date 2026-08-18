# Graph Report - .  (2026-08-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 879 nodes · 2020 edges · 75 communities (39 shown, 36 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 321 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `7daf9d67`
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
- Community 59
- Community 60
- Community 61
- Community 62
- Community 63
- Community 64
- Community 65
- Community 66
- Community 67
- Community 68
- Community 69
- Community 70
- Community 71
- Community 72
- Community 73
- Community 74

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 53 edges
2. `InMemoryGuardStore` - 40 edges
3. `ToolContext` - 39 edges
4. `DeterministicGuard` - 37 edges
5. `ToolCall` - 32 edges
6. `ScriptedPlanner` - 31 edges
7. `ItmanoCrmClient` - 31 edges
8. `CommandPlanner` - 30 edges
9. `GuardSettings` - 27 edges
10. `ToolResult` - 26 edges

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

## Communities (75 total, 36 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.06
Nodes (40): EstimateParams, _first_url(), GenerateImageParams, _Params, Any, ToolRegistry, Generation tools on the platform's Agent API. Two of them, and the pair is the…, Find the produced file, whichever shape the reply uses. The catalogue documents… (+32 more)

### Community 1 - "Community 1"
Cohesion: 0.11
Nodes (38): AgentReply, AuditEvent, AuditPhase, ExecutedCall, GuardDecision, Planner, PlanRequest, BaseModel (+30 more)

### Community 2 - "Community 2"
Cohesion: 0.10
Nodes (28): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+20 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (30): DuplicateToolError, BaseModel, StrEnum, Tool registry and calling protocol. This module is the contract every other…, Raised when two tools claim the same name., Raised when a name is looked up that was never registered., Raised on an attempt to register after the registry was frozen., What a tool does to the world. The guard treats these very differently:… (+22 more)

### Community 4 - "Community 4"
Cohesion: 0.15
Nodes (15): Agent, Plan, Runs one user turn to completion. ``max_iterations`` bounds plan/execute…, What the planner returns. A plan with no tool calls ends the turn; ``reply`` is…, A request to run one tool, as the planner emits it., Per-invocation identity and correlation. ``tenant_id`` is carried, never…, Name-to-implementation map, populated at startup and then frozen. Freezing…, Validate, run and time one call. Never raises. Anything a handler throws… (+7 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (20): AsyncClient, BaseException, ItmanoCrmSettings, Completion, GenerationError, _has_result(), Client for the platform's text generation endpoint. ``type=text`` is…, Price and validate a generation without spending anything. Free, and the honest… (+12 more)

### Community 6 - "Community 6"
Cohesion: 0.19
Nodes (17): DeterministicGuard, GuardSettings, The guard the orchestration loop consults before every call., SideEffect, call(), ToolContext, ToolSpec, A deployment that has not said yes cannot mutate anything. (+9 more)

### Community 7 - "Community 7"
Cohesion: 0.12
Nodes (14): CommandFastPath, Commands answered deterministically; everything else goes to a model. Ownership…, LlmPlanner, completion(), parse(), mock, An unbounded repair loop is a hole in the cost ceiling., A 500 is not a parse problem; repeating the same prompt will not fix it. (+6 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.14
Nodes (22): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+14 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (17): current_ledger(), ModelCall, Per-turn ledger of model calls. Cost and model choice are decisions this system…, One request to a language model, and what it cost., Collect every model call made inside this block., Add to the ledger if one is open. A no-op otherwise, never an error., record_model_call(), turn_ledger() (+9 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (14): Binding, BindingError, BindingTable, DenialReason, load_bindings(), Path, Decide whether this message may act, and for whom., Read the binding file. Any doubt is fatal rather than permissive. (+6 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (13): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., fixture, crm(), crm_registry(), ItmanoCrmSettings, Offline tests for the CRM adapter. Every response here comes from…, The planner sees descriptions and nothing else. (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (14): ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the…, contract_version(), load_contract(), Operation, operations(), Any (+6 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (17): agent_tool_operations(), Any, ToolRegistry, Registration of the CRM tools into a :class:`ToolRegistry`. Descriptions here…, Operation ids the contract marks as belonging in an agent's catalogue.…, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register() (+9 more)

### Community 15 - "Community 15"
Cohesion: 0.14
Nodes (13): AuditSink, Guard, NullAuditSink, ToolCall, ToolContext, ToolSpec, Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation. (+5 more)

### Community 16 - "Community 16"
Cohesion: 0.14
Nodes (15): GuardRule, intent_hash(), ToolCall, Deterministic limits in front of every action. Seven rules, checked in a fixed…, Which rule decided. Recorded on every decision, allow or deny., A stable fingerprint of *what is being attempted*. Arguments are canonicalised…, guard(), fixture (+7 more)

### Community 17 - "Community 17"
Cohesion: 0.15
Nodes (15): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated(), test_an_unknown_lead_maps_to_not_found(), test_identity_matches_what_we_expect() (+7 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (17): build_system_prompt(), _clip(), LlmPlanner, _PlannedCall, _PlannerOutput, BaseModel, PlanRequest, A planner built on a text model that has no native function calling. The… (+9 more)

### Community 19 - "Community 19"
Cohesion: 0.16
Nodes (13): CrmError, CrmResponse, _float_header(), _int_header(), Any, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift… (+5 more)

### Community 20 - "Community 20"
Cohesion: 0.23
Nodes (7): Any, CommandPlanner, Plan, PlanRequest, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim., Maps one command to one tool call, then renders the result.

### Community 21 - "Community 21"
Cohesion: 0.16
Nodes (8): InMemoryGuardStore, ToolContext, ToolSpec, Process-local implementation. Correct, and forgets everything on restart. Good…, Engage the kill switch. Synchronous on purpose: an operator action., deque, GuardDecision, Driven with explicit timestamps: a wall-clock window would be flaky.

### Community 22 - "Community 22"
Cohesion: 0.16
Nodes (13): Send one line per allowed call, before it runs., Keep the 'typing' state alive while the turn runs., What the last turn cost, and on which model. Model choice is a decision made on…, Record enough to write a binding, and nothing the sender said. The chat id is…, Long-poll for updates. Deployment swaps this for a webhook., Turns a Telegram message into an agent turn, or refuses it., run(), TelegramGateway (+5 more)

### Community 23 - "Community 23"
Cohesion: 0.21
Nodes (9): BindingTable, make_message(), The Telegram surface: who gets in, and whose tenant they act as., Distinct refusals would let someone probe which chats exist., The whole point of the boundary., Narration must never be able to kill what it narrates., TestAuthorisation, TestStepReporterSafety (+1 more)

### Community 24 - "Community 24"
Cohesion: 0.12
Nodes (9): LeadStage, parametrize, error_body(), Any, What a challenge page or a proxy error actually looks like., A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestErrorTranslation (+1 more)

### Community 25 - "Community 25"
Cohesion: 0.18
Nodes (6): mock, If this ever stops being null the tool description is a lie., The contract really does declare 201 here, not 200., TestReadPaths, TestStartupAssertion, TestWritePaths

### Community 26 - "Community 26"
Cohesion: 0.17
Nodes (10): BaseSettings, Which conversation may act for which tenant. This module is the authorization…, build_dispatcher(), Telegram surface: resolve the conversation, then hand off to the agent. Replies…, Configuration for the Telegram interface., TelegramSettings, Telegram interface: session to tenant mapping, and the command fast path., A deterministic planner for explicit commands. CONDUIT's orchestration loop… (+2 more)

### Community 27 - "Community 27"
Cohesion: 0.16
Nodes (6): Everything the rest of the system needs to know about a tool. Declared once by…, Adapter this tool belongs to, e.g. ``itmano_crm``., Argument schema, in the form a function-calling planner expects., Every spec, or only those of one adapter, sorted by name., What the planner is shown., ToolSpec

### Community 28 - "Community 28"
Cohesion: 0.27
Nodes (6): describe_step(), One line saying what the agent decided, before it acts on it. Shows the…, The 80-second wait is only bearable if it is announced., An expected wait is patience; an unexplained one reads as a crash. A range, not…, TestStepDescriptions, ToolCall

### Community 29 - "Community 29"
Cohesion: 0.38
Nodes (3): Plan, Telegram sends /leads@thebot in groups., TestCommandPlanner

### Community 30 - "Community 30"
Cohesion: 0.20
Nodes (6): GuardStore, Protocol, Record a write and return how many happened in the trailing hour., Record an intent and return how often it occurred inside the window., Counters and switches the rules read and write. Deliberately narrow, and every…, Record a call in this turn and return the running count, this one included.

### Community 31 - "Community 31"
Cohesion: 0.24
Nodes (7): Protocol, The shape of a tool implementation., Add a tool. Raises rather than silently replacing an existing name., Decorator form of :meth:`register`., RegisteredTool, ToolHandler, P

### Community 32 - "Community 32"
Cohesion: 0.25
Nodes (4): BaseModel, Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 33 - "Community 33"
Cohesion: 0.25
Nodes (3): won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 34 - "Community 34"
Cohesion: 0.36
Nodes (4): PlanRequest, Plain text, no parse mode. The demo tenant seeds exactly this case., A missing number is a number the reader invents., TestRendering

### Community 35 - "Community 35"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 36 - "Community 36"
Cohesion: 0.40
Nodes (5): Agent, Always calls the spy tool, then reports what it saw., spy_agent(), SpyTenantPlanner, ToolContext

### Community 37 - "Community 37"
Cohesion: 0.40
Nodes (3): A page of ten leads is ~3000 chars. Cutting it was the truncation bug., Silent truncation makes the model invent the rest or hedge blindly., TestResultClipping

### Community 38 - "Community 38"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **36 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 4` to `Community 27`, `Community 1`, `Community 3`, `Community 31`?**
  _High betweenness centrality (0.050) - this node is a cross-community bridge._
- **Why does `CommandPlanner` connect `Community 20` to `Community 34`, `Community 36`, `Community 23`, `Community 26`, `Community 28`, `Community 29`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 17` to `Community 32`, `Community 5`, `Community 12`, `Community 13`, `Community 19`, `Community 25`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ToolRegistry` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolRegistry` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `InMemoryGuardStore` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`InMemoryGuardStore` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ToolContext` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolContext` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `DeterministicGuard` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`DeterministicGuard` has 10 INFERRED edges - model-reasoned connections that need verification._