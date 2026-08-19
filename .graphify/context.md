# Graph Report - .  (2026-08-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 911 nodes · 2084 edges · 82 communities (30 shown, 52 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 312 edges (avg confidence: 0.51)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `3f2f7d51`
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

## Communities (82 total, 52 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (88): BaseModel, Agent, AgentReply, AuditEvent, AuditPhase, ExecutedCall, GuardDecision, Plan (+80 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (42): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (42): build_system_prompt(), _clip(), LlmPlanner, _PlannedCall, _PlannerOutput, A planner built on a text model that has no native function calling. The…, Trim only what is genuinely oversized, and say so when it happens. Silent…, Turns a transcript plus a tool catalogue into the next step. (+34 more)

### Community 3 - "Community 3"
Cohesion: 0.10
Nodes (28): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+20 more)

### Community 4 - "Community 4"
Cohesion: 0.07
Nodes (30): BaseSettings, Notified of every call the loop considered, with the guard's verdict. The point…, StepReporter, build_dispatcher(), BindingTable, Message, Telegram surface: resolve the conversation, then hand off to the agent. Replies…, Send one line per allowed call, before it runs. (+22 more)

### Community 5 - "Community 5"
Cohesion: 0.10
Nodes (15): Any, _transcript(), CommandFastPath, CommandPlanner, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim., Commands answered deterministically; everything else goes to a model. Ownership…, Maps one command to one tool call, then renders the result. (+7 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (23): Agent, BindingTable, Message, bindings(), make_message(), The Telegram surface: who gets in, and whose tenant they act as., Distinct refusals would let someone probe which chats exist., The whole point of the boundary. (+15 more)

### Community 7 - "Community 7"
Cohesion: 0.09
Nodes (26): agent_tool_operations(), Any, ToolRegistry, Registration of the CRM tools into a :class:`ToolRegistry`. Descriptions here…, Operation ids the contract marks as belonging in an agent's catalogue.…, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register() (+18 more)

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
Nodes (13): GenerateImageParams, Generation tools, offline. Every response here is simulated. Real generation…, The catalogue rejects over 800 characters. Better to never send it., Cost 1.20 RUB and 180 seconds to learn: the API says 'complete', not…, An optional field renders as "model?" in the planner prompt, and the planner…, A rouble spent does not come back. That is what WRITE is for., A clip is 149-590 RUB. Pricing is exposed; spending is not., TestArguments (+5 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (13): CrmError, CrmResponse, _float_header(), _int_header(), Any, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift… (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (16): GenerationError, _has_result(), Any, VibemarketologSettings, Price and validate a generation without spending anything. Free, and the honest…, Begin a paid generation. Always strict: malformed params are rejected before…, Poll until the generation finishes, fails, or we give up waiting. Giving up is…, A generation that has handed us a file is finished, whatever it is called. (+8 more)

### Community 14 - "Community 14"
Cohesion: 0.14
Nodes (13): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., fixture, ctx(), crm(), crm_registry(), ItmanoCrmSettings, Offline tests for the CRM adapter. Every response here comes from… (+5 more)

### Community 15 - "Community 15"
Cohesion: 0.12
Nodes (14): ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the…, contract_version(), load_contract(), Operation, operations(), Any (+6 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (15): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated(), test_an_unknown_lead_maps_to_not_found(), test_identity_matches_what_we_expect() (+7 more)

### Community 17 - "Community 17"
Cohesion: 0.27
Nodes (10): mock_candidate_prices(), mock, ToolRegistry, strict=true rejects bad params before the debit, not after., generate_image prices every candidate before spending. Free, but mocked., Belt and braces: never poll again over an unknown word for 'ready'., The demo posture: every read, plus exactly one chosen write., TestGenerating (+2 more)

### Community 18 - "Community 18"
Cohesion: 0.14
Nodes (10): BaseException, VibemarketologClient, ToolRegistry, Publish the generation tools. Call before ``registry.freeze()``., register(), Self, client(), fixture (+2 more)

### Community 19 - "Community 19"
Cohesion: 0.19
Nodes (12): Completion, Client for the platform's text generation endpoint. ``type=text`` is…, One synchronous text generation, recorded in the turn ledger., Configuration for the platform Agent API., VibemarketologSettings, Adapter for the platform's Agent API. Two roles, kept separate on purpose. The…, current_ledger(), ModelCall (+4 more)

### Community 20 - "Community 20"
Cohesion: 0.18
Nodes (6): mock, If this ever stops being null the tool description is a lie., The contract really does declare 201 here, not 200., TestReadPaths, TestStartupAssertion, TestWritePaths

### Community 21 - "Community 21"
Cohesion: 0.13
Nodes (10): AuditSink, Guard, Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation., GuardStore, Record a write and return how many happened in the trailing hour., Record an intent and return how often it occurred inside the window., Counters and switches the rules read and write. Deliberately narrow, and every… (+2 more)

### Community 22 - "Community 22"
Cohesion: 0.20
Nodes (6): parametrize, The catalogue documents several conventions. Look, do not guess., error_body(), Any, What a challenge page or a proxy error actually looks like., TestErrorTranslation

### Community 23 - "Community 23"
Cohesion: 0.29
Nodes (3): Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 24 - "Community 24"
Cohesion: 0.25
Nodes (4): LeadStage, A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestStageAliases

### Community 25 - "Community 25"
Cohesion: 0.25
Nodes (3): won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 26 - "Community 26"
Cohesion: 0.33
Nodes (3): NullAuditSink, Discards everything. Only acceptable in tests and phase-1 scaffolding., Guard, audit the intent, run, audit the outcome. In that order.

### Community 27 - "Community 27"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 28 - "Community 28"
Cohesion: 0.40
Nodes (3): AsyncClient, ItmanoCrmSettings, ToolErrorCode

### Community 29 - "Community 29"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **52 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ItmanoCrmClient` connect `Community 16` to `Community 12`, `Community 14`, `Community 15`, `Community 18`, `Community 20`, `Community 23`, `Community 28`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Why does `InMemoryGuardStore` connect `Community 1` to `Community 3`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ToolRegistry` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolRegistry` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `InMemoryGuardStore` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`InMemoryGuardStore` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `DeterministicGuard` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`DeterministicGuard` has 11 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ToolContext` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolContext` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 12 inferred relationships involving `ToolCall` (e.g. with `ExplodingPlanner` and `PermissiveGuard`) actually correct?**
  _`ToolCall` has 12 INFERRED edges - model-reasoned connections that need verification._