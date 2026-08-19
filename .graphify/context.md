# Graph Report - .  (2026-08-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 931 nodes · 2138 edges · 91 communities (39 shown, 52 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 330 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `0c49a567`
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
- Community 75
- Community 76
- Community 77
- Community 78
- Community 79
- Community 80
- Community 81
- Community 82
- Community 83
- Community 84
- Community 85
- Community 86
- Community 87
- Community 88
- Community 89
- Community 90

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 53 edges
2. `InMemoryGuardStore` - 45 edges
3. `DeterministicGuard` - 42 edges
4. `ToolContext` - 39 edges
5. `ToolCall` - 32 edges
6. `GuardSettings` - 32 edges
7. `ScriptedPlanner` - 31 edges
8. `ItmanoCrmClient` - 31 edges
9. `TelegramGateway` - 31 edges
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

## Communities (91 total, 52 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.08
Nodes (42): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+34 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (42): BaseException, BaseSettings, Completion, GenerationError, _has_result(), Any, VibemarketologSettings, Client for the platform's text generation endpoint. ``type=text`` is… (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (26): Any, Argument schema, in the form a function-calling planner expects., What the planner is shown., CommandFastPath, CommandPlanner, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim., Commands answered deterministically; everything else goes to a model. Ownership… (+18 more)

### Community 3 - "Community 3"
Cohesion: 0.08
Nodes (31): DuplicateToolError, BaseModel, StrEnum, Tool registry and calling protocol. This module is the contract every other…, Raised when two tools claim the same name., Raised when a name is looked up that was never registered., Raised on an attempt to register after the registry was frozen., What a tool does to the world. The guard treats these very differently:… (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (28): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+20 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (24): NullAuditSink, Discards everything. Only acceptable in tests and phase-1 scaffolding., Guard, audit the intent, run, audit the outcome. In that order., _as_executed(), describe_step(), One line saying what the agent decided, before it acts on it. Shows the…, The arguments as the tool will actually receive them, defaults and all., GuardDecision (+16 more)

### Community 6 - "Community 6"
Cohesion: 0.15
Nodes (15): Agent, Plan, Runs one user turn to completion. ``max_iterations`` bounds plan/execute…, What the planner returns. A plan with no tool calls ends the turn; ``reply`` is…, A request to run one tool, as the planner emits it., Per-invocation identity and correlation. ``tenant_id`` is carried, never…, Name-to-implementation map, populated at startup and then frozen. Freezing…, Validate, run and time one call. Never raises. Anything a handler throws… (+7 more)

### Community 7 - "Community 7"
Cohesion: 0.15
Nodes (31): BaseModel, AgentReply, AuditEvent, AuditPhase, ExecutedCall, GuardDecision, Planner, PlanRequest (+23 more)

### Community 8 - "Community 8"
Cohesion: 0.07
Nodes (35): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+27 more)

### Community 9 - "Community 9"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (15): Binding, BindingError, BindingTable, DenialReason, load_bindings(), Path, Which conversation may act for which tenant. This module is the authorization…, Decide whether this message may act, and for whom. (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.18
Nodes (14): Turns a Telegram message into an agent turn, or refuses it., TelegramGateway, make_message(), BindingTable, Message, Distinct refusals would let someone probe which chats exist., The whole point of the boundary., Narration must never be able to kill what it narrates. (+6 more)

### Community 12 - "Community 12"
Cohesion: 0.11
Nodes (13): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., fixture, crm(), crm_registry(), ItmanoCrmSettings, Offline tests for the CRM adapter. Every response here comes from…, What a challenge page or a proxy error actually looks like. (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (14): ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the…, contract_version(), load_contract(), Operation, operations(), Any (+6 more)

### Community 14 - "Community 14"
Cohesion: 0.25
Nodes (11): LlmPlanner, Turns a transcript plus a tool catalogue into the next step., mock, completion(), An unbounded repair loop is a hole in the cost ceiling., A 500 is not a parse problem; repeating the same prompt will not fix it., The safety net: if the model API is down, commands must still answer., request_for() (+3 more)

### Community 15 - "Community 15"
Cohesion: 0.11
Nodes (12): AuditSink, Guard, Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation., Notified of every call the loop considered, with the guard's verdict. The point…, StepReporter, GuardStore, Record a write and return how many happened in the trailing hour. (+4 more)

### Community 16 - "Community 16"
Cohesion: 0.18
Nodes (12): CrmError, CrmResponse, _float_header(), _int_header(), Any, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift… (+4 more)

### Community 17 - "Community 17"
Cohesion: 0.18
Nodes (12): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated(), test_an_unknown_lead_maps_to_not_found(), test_identity_matches_what_we_expect() (+4 more)

### Community 18 - "Community 18"
Cohesion: 0.17
Nodes (11): build_dispatcher(), Agent, BindingTable, Telegram surface: resolve the conversation, then hand off to the agent. Replies…, Long-poll for updates. Deployment swaps this for a webhook., run(), Configuration for the Telegram interface., Telegram interface: session to tenant mapping, and the command fast path. (+3 more)

### Community 19 - "Community 19"
Cohesion: 0.16
Nodes (10): _message_kind(), Message, Send one line per allowed call, before it runs., Keep the 'typing' state alive while the turn runs., What the last turn cost, and on which model. Model choice is a decision made on…, Record enough to write a binding, and nothing the sender said. The chat id is…, Name what arrived, for the log. Nothing here reaches the sender., Resolution (+2 more)

### Community 20 - "Community 20"
Cohesion: 0.14
Nodes (7): LeadStage, parametrize, The catalogue documents several conventions. Look, do not guess., TestUrlExtraction, A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestStageAliases

### Community 21 - "Community 21"
Cohesion: 0.23
Nodes (5): parse(), Models wrap JSON in fences constantly, whatever the instructions say., Code catches this, not the model's good behaviour., A model adding commentary keys should not fail the whole plan., TestParsing

### Community 22 - "Community 22"
Cohesion: 0.26
Nodes (8): build_system_prompt(), One tool as the planner sees it: signature, purpose, per-argument notes. The…, _render_tool(), If the valid values are not in the prompt the model has to guess., Field descriptions used to be dropped from the prompt entirely. Only the tool-…, TestParameterNotesReachThePlanner, TestSystemPrompt, ToolSpec

### Community 23 - "Community 23"
Cohesion: 0.19
Nodes (10): _clip(), Trim only what is genuinely oversized, and say so when it happens. Silent…, planner(), The planner's parser, offline. Without native function calling the model…, A page of ten leads is ~3000 chars. Cutting it was the truncation bug., Silent truncation makes the model invent the rest or hedge blindly., settings(), TestNoParamsTool (+2 more)

### Community 24 - "Community 24"
Cohesion: 0.20
Nodes (7): detect_language(), Name the language to answer in, or None when it is not clear. Deliberately…, PlanRequest, Decided in code, not left to a rule in a cached prompt. Three live failures…, leads' and 'en' occur in English too; a single hit proves nothing., A description saying "in English or Russian" seeded Russian replies to English…, TestReplyLanguage

### Community 25 - "Community 25"
Cohesion: 0.25
Nodes (8): _PlannedCall, _PlannerOutput, BaseModel, PlanRequest, A planner built on a text model that has no native function calling. The…, Strict. A near-miss is a failure, not something to bend into shape., _strip_fences(), _transcript()

### Community 26 - "Community 26"
Cohesion: 0.27
Nodes (7): main(), percentile(), Measure what a CRM tool call actually costs, through the real invocation path.…, timed(), The planner sees descriptions and nothing else., TestRegistration, ToolRegistry

### Community 27 - "Community 27"
Cohesion: 0.18
Nodes (6): error_body(), Any, The failure that actually happens at startup is a transient challenge from the…, A bad token is a definite answer. Repeating it just wastes startup., Retrying must not soften the check it exists for., TestVerifyRetry

### Community 28 - "Community 28"
Cohesion: 0.24
Nodes (7): Protocol, The shape of a tool implementation., Add a tool. Raises rather than silently replacing an existing name., Decorator form of :meth:`register`., RegisteredTool, ToolHandler, P

### Community 29 - "Community 29"
Cohesion: 0.22
Nodes (8): bindings(), Agent, The Telegram surface: who gets in, and whose tenant they act as., The planner may say "lost"; the CRM has no such stage. Showing the raw word…, Always calls the spy tool, then reports what it saw., spy_agent(), SpyTenantPlanner, TestArgumentsAreShownAsExecuted

### Community 30 - "Community 30"
Cohesion: 0.33
Nodes (5): GenerateImageParams, The catalogue rejects over 800 characters. Better to never send it., An optional field renders as "model?" in the planner prompt, and the planner…, TestArguments, TestModelIsAlwaysChosen

### Community 31 - "Community 31"
Cohesion: 0.25
Nodes (4): Everything the rest of the system needs to know about a tool. Declared once by…, Adapter this tool belongs to, e.g. ``itmano_crm``., Every spec, or only those of one adapter, sorted by name., ToolSpec

### Community 32 - "Community 32"
Cohesion: 0.29
Nodes (3): Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 33 - "Community 33"
Cohesion: 0.25
Nodes (3): won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 34 - "Community 34"
Cohesion: 0.39
Nodes (3): The 80-second wait is only bearable if it is announced., An expected wait is patience; an unexplained one reads as a crash. A range, not…, TestStepDescriptions

### Community 35 - "Community 35"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 37 - "Community 37"
Cohesion: 0.47
Nodes (3): A refusal is the most interesting thing a turn can contain. Announcing it only…, Nothing was spent, so the money warning would be a lie., TestRefusalsAreAnnounced

### Community 38 - "Community 38"
Cohesion: 0.40
Nodes (3): AsyncClient, ItmanoCrmSettings, ToolErrorCode

### Community 39 - "Community 39"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **52 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TelegramGateway` connect `Community 11` to `Community 2`, `Community 34`, `Community 37`, `Community 18`, `Community 19`, `Community 29`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `ToolRegistry` connect `Community 6` to `Community 2`, `Community 3`, `Community 7`, `Community 28`, `Community 31`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 17` to `Community 32`, `Community 1`, `Community 38`, `Community 12`, `Community 13`, `Community 16`, `Community 27`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ToolRegistry` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolRegistry` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `InMemoryGuardStore` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`InMemoryGuardStore` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `DeterministicGuard` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`DeterministicGuard` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ToolContext` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolContext` has 14 INFERRED edges - model-reasoned connections that need verification._