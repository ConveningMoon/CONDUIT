# Graph Report - .  (2026-08-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 903 nodes · 2162 edges · 77 communities (33 shown, 44 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 387 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bb9e58ef`
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

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 53 edges
2. `InMemoryGuardStore` - 40 edges
3. `ToolContext` - 39 edges
4. `Agent` - 38 edges
5. `DeterministicGuard` - 37 edges
6. `Plan` - 37 edges
7. `ToolCall` - 32 edges
8. `CommandPlanner` - 32 edges
9. `ScriptedPlanner` - 31 edges
10. `ItmanoCrmClient` - 31 edges

## Surprising Connections (you probably didn't know these)
- `EchoParams` --uses--> `SideEffect`  [INFERRED]
  tests/conftest.py → conduit/core/tools.py
- `NoParams` --uses--> `SideEffect`  [INFERRED]
  tests/conftest.py → conduit/core/tools.py
- `PermissiveGuard` --uses--> `SideEffect`  [INFERRED]
  tests/test_agent.py → conduit/core/tools.py
- `ScriptedPlanner` --uses--> `SideEffect`  [INFERRED]
  tests/test_agent.py → conduit/core/tools.py
- `TestInvoke` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py

## Import Cycles
- None detected.

## Communities (77 total, 44 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (39): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+31 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (43): build_system_prompt(), _clip(), LlmPlanner, Plan, PlanRequest, ToolSpec, Trim only what is genuinely oversized, and say so when it happens. Silent…, Turns a transcript plus a tool catalogue into the next step. (+35 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (40): BaseException, BaseSettings, Completion, GenerationError, _has_result(), Any, VibemarketologSettings, Client for the platform's text generation endpoint. ``type=text`` is… (+32 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (27): Any, Argument schema, in the form a function-calling planner expects., What the planner is shown., _as_executed(), CommandFastPath, CommandPlanner, A deterministic planner for explicit commands. CONDUIT's orchestration loop…, Turn the tool result at the end of the transcript into a reply. (+19 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (28): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+20 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (26): _first_url(), GenerateImageParams, Any, Find the produced file, whichever shape the reply uses. The catalogue documents…, mock_candidate_prices(), mock, ToolRegistry, Generation tools, offline. Every response here is simulated. Real generation… (+18 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (29): BaseModel, Agent, AgentReply, ExecutedCall, GuardDecision, Plan, PlanRequest, Orchestration loop: intent, plan, guard, execute, report. The loop owns the… (+21 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (30): DuplicateToolError, BaseModel, Tool registry and calling protocol. This module is the contract every other…, Everything the rest of the system needs to know about a tool. Declared once by…, Adapter this tool belongs to, e.g. ``itmano_crm``., Raised when two tools claim the same name., Raised when a name is looked up that was never registered., Raised on an attempt to register after the registry was frozen. (+22 more)

### Community 8 - "Community 8"
Cohesion: 0.13
Nodes (14): Default guard until ``conduit.core.guard`` lands: reads pass, writes do not.…, ReadOnlyGuard, A request to run one tool, as the planner emits it., Per-invocation identity and correlation. ``tenant_id`` is carried, never…, Name-to-implementation map, populated at startup and then frozen. Freezing…, ToolCall, ToolContext, ToolRegistry (+6 more)

### Community 9 - "Community 9"
Cohesion: 0.09
Nodes (16): NullAuditSink, ToolCall, ToolContext, ToolSpec, Discards everything. Only acceptable in tests and phase-1 scaffolding., Guard, audit the intent, run, audit the outcome. In that order., describe_step(), One line saying what the agent decided, before it acts on it. Shows the… (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.09
Nodes (14): mock, error_body(), Any, If this ever stops being null the tool description is a lie., What a challenge page or a proxy error actually looks like., The contract really does declare 201 here, not 200., The failure that actually happens at startup is a transient challenge from the…, A bad token is a definite answer. Repeating it just wastes startup. (+6 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (15): Binding, BindingError, BindingTable, DenialReason, load_bindings(), Path, Which conversation may act for which tenant. This module is the authorization…, Decide whether this message may act, and for whom. (+7 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (22): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+14 more)

### Community 14 - "Community 14"
Cohesion: 0.13
Nodes (15): CrmResponse, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, A successful call, plus the headers worth carrying forward., Configuration for the ITMANO CRM adapter. Everything arrives via env vars., contract_version(), load_contract(), Operation, operations() (+7 more)

### Community 15 - "Community 15"
Cohesion: 0.15
Nodes (12): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., fixture, crm(), crm_registry(), ItmanoCrmSettings, Offline tests for the CRM adapter. Every response here comes from…, The planner sees descriptions and nothing else. (+4 more)

### Community 16 - "Community 16"
Cohesion: 0.25
Nodes (17): AuditEvent, AuditPhase, ``INTENT`` is written before the call runs, ``OUTCOME`` after., One record in the action log. Serialisable, no live objects., StopReason, StrEnum, What a tool does to the world. The guard treats these very differently:…, Outcome of an invocation, from the caller's point of view. (+9 more)

### Community 17 - "Community 17"
Cohesion: 0.15
Nodes (10): CrmError, _float_header(), _int_header(), Any, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift…, A call that did not succeed, already in CONDUIT's error vocabulary., Exception (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (16): agent_tool_operations(), Any, ToolRegistry, Registration of the CRM tools into a :class:`ToolRegistry`. Descriptions here…, Operation ids the contract marks as belonging in an agent's catalogue.…, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register() (+8 more)

### Community 19 - "Community 19"
Cohesion: 0.21
Nodes (13): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., ItmanoCrmSettings, Connection details plus the assertion that guards against pointing here at the…, client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated() (+5 more)

### Community 21 - "Community 21"
Cohesion: 0.23
Nodes (9): Turns a Telegram message into an agent turn, or refuses it., TelegramGateway, bindings(), make_message(), BindingTable, Message, Distinct refusals would let someone probe which chats exist., The whole point of the boundary. (+1 more)

### Community 22 - "Community 22"
Cohesion: 0.19
Nodes (10): build_dispatcher(), BindingTable, Telegram surface: resolve the conversation, then hand off to the agent. Replies…, Long-poll for updates. Deployment swaps this for a webhook., run(), Configuration for the Telegram interface., TelegramSettings, Telegram interface: session to tenant mapping, and the command fast path. (+2 more)

### Community 23 - "Community 23"
Cohesion: 0.20
Nodes (7): Message, Send one line per allowed call, before it runs., Keep the 'typing' state alive while the turn runs., What the last turn cost, and on which model. Model choice is a decision made on…, Record enough to write a binding, and nothing the sender said. The chat id is…, Resolution, Task

### Community 24 - "Community 24"
Cohesion: 0.20
Nodes (9): AuditSink, Guard, Planner, Turns a transcript plus a tool catalogue into the next step., Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation., Notified of each call the guard has allowed, just before it runs. The point is…, StepReporter (+1 more)

### Community 25 - "Community 25"
Cohesion: 0.20
Nodes (6): GuardStore, Protocol, Record a write and return how many happened in the trailing hour., Record an intent and return how often it occurred inside the window., Counters and switches the rules read and write. Deliberately narrow, and every…, Record a call in this turn and return the running count, this one included.

### Community 26 - "Community 26"
Cohesion: 0.29
Nodes (3): Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 27 - "Community 27"
Cohesion: 0.25
Nodes (3): won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 28 - "Community 28"
Cohesion: 0.24
Nodes (7): Protocol, The shape of a tool implementation., Add a tool. Raises rather than silently replacing an existing name., Decorator form of :meth:`register`., RegisteredTool, ToolHandler, P

### Community 29 - "Community 29"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 30 - "Community 30"
Cohesion: 0.33
Nodes (3): LeadStage, parametrize, The catalogue documents several conventions. Look, do not guess.

### Community 31 - "Community 31"
Cohesion: 0.33
Nodes (3): A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestStageAliases

### Community 32 - "Community 32"
Cohesion: 0.40
Nodes (3): AsyncClient, ItmanoCrmSettings, ToolErrorCode

### Community 33 - "Community 33"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **44 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 8` to `Community 3`, `Community 6`, `Community 7`, `Community 16`, `Community 28`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 19` to `Community 32`, `Community 2`, `Community 10`, `Community 14`, `Community 15`, `Community 17`, `Community 26`?**
  _High betweenness centrality (0.038) - this node is a cross-community bridge._
- **Why does `InMemoryGuardStore` connect `Community 0` to `Community 4`?**
  _High betweenness centrality (0.037) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ToolRegistry` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolRegistry` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `InMemoryGuardStore` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`InMemoryGuardStore` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ToolContext` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolContext` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 18 inferred relationships involving `Agent` (e.g. with `TelegramGateway` and `ExplodingPlanner`) actually correct?**
  _`Agent` has 18 INFERRED edges - model-reasoned connections that need verification._