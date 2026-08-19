# Graph Report - .  (2026-08-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 911 nodes · 2093 edges · 79 communities (30 shown, 49 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 319 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `08d7bea6`
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

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 53 edges
2. `InMemoryGuardStore` - 45 edges
3. `DeterministicGuard` - 42 edges
4. `ToolContext` - 39 edges
5. `ToolCall` - 32 edges
6. `GuardSettings` - 32 edges
7. `ScriptedPlanner` - 31 edges
8. `ItmanoCrmClient` - 31 edges
9. `Agent` - 27 edges
10. `ToolResult` - 26 edges

## Surprising Connections (you probably didn't know these)
- `TestThroughTheLoop` --uses--> `AuditRecord`  [INFERRED]
  tests/test_audit.py → conduit/core/audit.py
- `TestThroughTheLoop` --uses--> `InMemoryAuditStore`  [INFERRED]
  tests/test_audit.py → conduit/core/audit.py
- `TestThroughTheLoop` --uses--> `HashChainAuditSink`  [INFERRED]
  tests/test_audit.py → conduit/core/audit.py
- `TestChaining` --uses--> `DeterministicGuard`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestChaining` --uses--> `GuardSettings`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py

## Import Cycles
- None detected.

## Communities (79 total, 49 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (87): BaseModel, Agent, AgentReply, AuditEvent, AuditPhase, ExecutedCall, GuardDecision, Plan (+79 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (45): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+37 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (38): build_system_prompt(), _clip(), LlmPlanner, ToolSpec, Trim only what is genuinely oversized, and say so when it happens. Silent…, Turns a transcript plus a tool catalogue into the next step., One tool as the planner sees it: signature, purpose, per-argument notes. The…, _render_tool() (+30 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (31): Any, Argument schema, in the form a function-calling planner expects., What the planner is shown., _as_executed(), CommandFastPath, CommandPlanner, describe_step(), A deterministic planner for explicit commands. CONDUIT's orchestration loop… (+23 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (25): Agent, BindingTable, Message, bindings(), make_message(), The Telegram surface: who gets in, and whose tenant they act as., Distinct refusals would let someone probe which chats exist., The whole point of the boundary. (+17 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (28): _first_url(), Any, Find the produced file, whichever shape the reply uses. The catalogue documents…, NullAuditSink, Discards everything. Only acceptable in tests and phase-1 scaffolding., Guard, audit the intent, run, audit the outcome. In that order., client(), mock_candidate_prices() (+20 more)

### Community 6 - "Community 6"
Cohesion: 0.06
Nodes (32): BaseSettings, AuditSink, Guard, Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation., Notified of every call the loop considered, with the guard's verdict. The point…, StepReporter, GuardStore (+24 more)

### Community 7 - "Community 7"
Cohesion: 0.11
Nodes (25): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+17 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.12
Nodes (15): Binding, BindingError, BindingTable, DenialReason, load_bindings(), Path, Which conversation may act for which tenant. This module is the authorization…, Decide whether this message may act, and for whom. (+7 more)

### Community 10 - "Community 10"
Cohesion: 0.14
Nodes (22): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+14 more)

### Community 11 - "Community 11"
Cohesion: 0.13
Nodes (15): CrmResponse, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, A successful call, plus the headers worth carrying forward., Configuration for the ITMANO CRM adapter. Everything arrives via env vars., contract_version(), load_contract(), Operation, operations() (+7 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (9): mock, If this ever stops being null the tool description is a lie., The contract really does declare 201 here, not 200., The failure that actually happens at startup is a transient challenge from the…, Retrying must not soften the check it exists for., TestReadPaths, TestStartupAssertion, TestVerifyRetry (+1 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (17): agent_tool_operations(), Any, ToolRegistry, Registration of the CRM tools into a :class:`ToolRegistry`. Descriptions here…, Operation ids the contract marks as belonging in an agent's catalogue.…, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register() (+9 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (12): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., fixture, crm(), crm_registry(), ItmanoCrmSettings, Offline tests for the CRM adapter. Every response here comes from…, The planner sees descriptions and nothing else. (+4 more)

### Community 15 - "Community 15"
Cohesion: 0.19
Nodes (10): CrmError, _float_header(), _int_header(), Any, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift…, A call that did not succeed, already in CONDUIT's error vocabulary., Exception (+2 more)

### Community 16 - "Community 16"
Cohesion: 0.21
Nodes (13): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., ItmanoCrmSettings, Connection details plus the assertion that guards against pointing here at the…, client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated() (+5 more)

### Community 17 - "Community 17"
Cohesion: 0.16
Nodes (8): _has_result(), Any, Price and validate a generation without spending anything. Free, and the honest…, Begin a paid generation. Always strict: malformed params are rejected before…, Poll until the generation finishes, fails, or we give up waiting. Giving up is…, A generation that has handed us a file is finished, whatever it is called., VibemarketologClient, Self

### Community 18 - "Community 18"
Cohesion: 0.17
Nodes (7): LeadStage, parametrize, error_body(), Any, What a challenge page or a proxy error actually looks like., A bad token is a definite answer. Repeating it just wastes startup., TestErrorTranslation

### Community 19 - "Community 19"
Cohesion: 0.27
Nodes (9): Completion, Client for the platform's text generation endpoint. ``type=text`` is…, One synchronous text generation, recorded in the turn ledger., current_ledger(), ModelCall, Per-turn ledger of model calls. Cost and model choice are decisions this system…, One request to a language model, and what it cost., Add to the ledger if one is open. A no-op otherwise, never an error. (+1 more)

### Community 20 - "Community 20"
Cohesion: 0.23
Nodes (9): _PlannedCall, _PlannerOutput, BaseModel, Plan, PlanRequest, A planner built on a text model that has no native function calling. The…, Strict. A near-miss is a failure, not something to bend into shape., _strip_fences() (+1 more)

### Community 21 - "Community 21"
Cohesion: 0.27
Nodes (7): GenerationError, VibemarketologSettings, The platform did not return a usable completion., EstimateParams, _Params, BaseModel, Generation tools on the platform's Agent API. Two of them, and the pair is the…

### Community 22 - "Community 22"
Cohesion: 0.33
Nodes (5): GenerateImageParams, The catalogue rejects over 800 characters. Better to never send it., An optional field renders as "model?" in the planner prompt, and the planner…, TestArguments, TestModelIsAlwaysChosen

### Community 23 - "Community 23"
Cohesion: 0.29
Nodes (3): Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 24 - "Community 24"
Cohesion: 0.29
Nodes (6): Configuration for the platform Agent API., VibemarketologSettings, Adapter for the platform's Agent API. Two roles, kept separate on purpose. The…, ToolRegistry, Publish the generation tools. Call before ``registry.freeze()``., register()

### Community 25 - "Community 25"
Cohesion: 0.25
Nodes (3): won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 27 - "Community 27"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 28 - "Community 28"
Cohesion: 0.33
Nodes (3): A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestStageAliases

### Community 29 - "Community 29"
Cohesion: 0.40
Nodes (3): AsyncClient, ItmanoCrmSettings, ToolErrorCode

### Community 30 - "Community 30"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **49 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 0` to `Community 3`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `InMemoryGuardStore` connect `Community 1` to `Community 7`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 16` to `Community 11`, `Community 12`, `Community 14`, `Community 15`, `Community 17`, `Community 18`, `Community 23`, `Community 26`, `Community 29`?**
  _High betweenness centrality (0.039) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ToolRegistry` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolRegistry` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `InMemoryGuardStore` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`InMemoryGuardStore` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `DeterministicGuard` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`DeterministicGuard` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ToolContext` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolContext` has 14 INFERRED edges - model-reasoned connections that need verification._