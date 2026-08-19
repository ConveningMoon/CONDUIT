# Graph Report - .  (2026-08-20)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 937 nodes · 2162 edges · 80 communities (29 shown, 51 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 325 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3856b196`
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

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 53 edges
2. `InMemoryGuardStore` - 45 edges
3. `DeterministicGuard` - 42 edges
4. `ToolContext` - 39 edges
5. `ToolCall` - 32 edges
6. `GuardSettings` - 32 edges
7. `TelegramGateway` - 32 edges
8. `ScriptedPlanner` - 31 edges
9. `ItmanoCrmClient` - 31 edges
10. `ToolResult` - 26 edges

## Surprising Connections (you probably didn't know these)
- `TestChaining` --uses--> `DeterministicGuard`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestChaining` --uses--> `GuardSettings`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestChaining` --uses--> `InMemoryGuardStore`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestTampering` --uses--> `DeterministicGuard`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py
- `TestTampering` --uses--> `GuardSettings`  [INFERRED]
  tests/test_audit.py → conduit/core/guard.py

## Import Cycles
- None detected.

## Communities (80 total, 51 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (85): BaseModel, Agent, AgentReply, AuditEvent, AuditPhase, ExecutedCall, GuardDecision, Plan (+77 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (42): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (44): Agent, BindingTable, build_dispatcher(), _message_kind(), Send one line per allowed call, before it runs., Keep the 'typing' state alive while the turn runs., What the last turn cost, and on which model. Model choice is a decision made on…, Record enough to write a binding, and nothing the sender said. The chat id is… (+36 more)

### Community 3 - "Community 3"
Cohesion: 0.05
Nodes (33): Any, Argument schema, in the form a function-calling planner expects., What the planner is shown., Telegram interface: session to tenant mapping, and the command fast path., _as_executed(), CommandFastPath, CommandPlanner, describe_step() (+25 more)

### Community 4 - "Community 4"
Cohesion: 0.05
Nodes (40): BaseException, BaseSettings, Completion, GenerationError, _has_result(), Any, VibemarketologSettings, Client for the platform's text generation endpoint. ``type=text`` is… (+32 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (28): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+20 more)

### Community 6 - "Community 6"
Cohesion: 0.07
Nodes (35): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+27 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 8 - "Community 8"
Cohesion: 0.15
Nodes (15): mock, mock_candidate_prices(), ToolRegistry, strict=true rejects bad params before the debit, not after., generate_image prices every candidate before spending. Free, but mocked., Belt and braces: never poll again over an unknown word for 'ready'., /debug claims to report what the turn cost. It counted only the planning calls,…, The platform refunds a failure, so charging it to the turn would overstate the… (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (16): LlmPlanner, Turns a transcript plus a tool catalogue into the next step., completion(), planner(), The planner's parser, offline. Without native function calling the model…, An unbounded repair loop is a hole in the cost ceiling., A 500 is not a parse problem; repeating the same prompt will not fix it., The safety net: if the model API is down, commands must still answer. (+8 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (15): Binding, BindingError, BindingTable, DenialReason, load_bindings(), Path, Which conversation may act for which tenant. This module is the authorization…, Decide whether this message may act, and for whom. (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (13): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., crm(), error_body(), Any, ItmanoCrmSettings, Offline tests for the CRM adapter. Every response here comes from…, What a challenge page or a proxy error actually looks like. (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (16): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated(), test_an_unknown_lead_maps_to_not_found(), test_identity_matches_what_we_expect() (+8 more)

### Community 13 - "Community 13"
Cohesion: 0.14
Nodes (12): build_system_prompt(), One tool as the planner sees it: signature, purpose, per-argument notes. The…, _render_tool(), NullAuditSink, Discards everything. Only acceptable in tests and phase-1 scaffolding., Guard, audit the intent, run, audit the outcome. In that order., If the valid values are not in the prompt the model has to guess., Field descriptions used to be dropped from the prompt entirely. Only the tool-… (+4 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (14): ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the…, contract_version(), load_contract(), Operation, operations(), Any (+6 more)

### Community 15 - "Community 15"
Cohesion: 0.10
Nodes (14): AuditSink, Guard, Planner, Turns a transcript plus a tool catalogue into the next step., Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation., Notified of every call the loop considered, with the guard's verdict. The point…, StepReporter (+6 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (10): CrmError, _float_header(), _int_header(), Any, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift…, A call that did not succeed, already in CONDUIT's error vocabulary., Exception (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.15
Nodes (13): _clip(), _PlannedCall, _PlannerOutput, BaseModel, PlanRequest, A planner built on a text model that has no native function calling. The…, Trim only what is genuinely oversized, and say so when it happens. Silent…, Strict. A near-miss is a failure, not something to bend into shape. (+5 more)

### Community 18 - "Community 18"
Cohesion: 0.17
Nodes (13): GenerateImageParams, fixture, client(), VibemarketologClient, Generation tools, offline. Every response here is simulated. Real generation…, The catalogue rejects over 800 characters. Better to never send it., Cost 1.20 RUB and 180 seconds to learn: the API says 'complete', not…, An optional field renders as "model?" in the planner prompt, and the planner… (+5 more)

### Community 19 - "Community 19"
Cohesion: 0.14
Nodes (7): LeadStage, parametrize, The catalogue documents several conventions. Look, do not guess., TestUrlExtraction, A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestStageAliases

### Community 20 - "Community 20"
Cohesion: 0.23
Nodes (5): parse(), Models wrap JSON in fences constantly, whatever the instructions say., Code catches this, not the model's good behaviour., A model adding commentary keys should not fail the whole plan., TestParsing

### Community 21 - "Community 21"
Cohesion: 0.20
Nodes (7): detect_language(), Name the language to answer in, or None when it is not clear. Deliberately…, PlanRequest, Decided in code, not left to a rule in a cached prompt. Three live failures…, leads' and 'en' occur in English too; a single hit proves nothing., A description saying "in English or Russian" seeded Russian replies to English…, TestReplyLanguage

### Community 22 - "Community 22"
Cohesion: 0.24
Nodes (8): main(), percentile(), Measure what a CRM tool call actually costs, through the real invocation path.…, timed(), crm_registry(), The planner sees descriptions and nothing else., TestRegistration, ToolRegistry

### Community 23 - "Community 23"
Cohesion: 0.24
Nodes (8): CrmResponse, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, A successful call, plus the headers worth carrying forward., from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 24 - "Community 24"
Cohesion: 0.29
Nodes (3): Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 25 - "Community 25"
Cohesion: 0.25
Nodes (3): won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 26 - "Community 26"
Cohesion: 0.29
Nodes (3): A rouble spent does not come back. That is what WRITE is for., A clip is 149-590 RUB. Pricing is exposed; spending is not., TestSideEffects

### Community 27 - "Community 27"
Cohesion: 0.40
Nodes (3): AsyncClient, ItmanoCrmSettings, ToolErrorCode

### Community 28 - "Community 28"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **51 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `TelegramGateway` connect `Community 2` to `Community 3`, `Community 4`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Why does `ToolRegistry` connect `Community 0` to `Community 3`?**
  _High betweenness centrality (0.045) - this node is a cross-community bridge._
- **Why does `ModelCall` connect `Community 4` to `Community 18`, `Community 2`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ToolRegistry` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolRegistry` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `InMemoryGuardStore` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`InMemoryGuardStore` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `DeterministicGuard` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`DeterministicGuard` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ToolContext` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolContext` has 14 INFERRED edges - model-reasoned connections that need verification._