# Graph Report - .  (2026-08-19)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 922 nodes · 2105 edges · 84 communities (29 shown, 55 thin omitted)
- Extraction: 85% EXTRACTED · 15% INFERRED · 0% AMBIGUOUS · INFERRED: 322 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `db99cae7`
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

## Communities (84 total, 55 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (87): BaseModel, Agent, AgentReply, AuditEvent, AuditPhase, ExecutedCall, GuardDecision, Plan (+79 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (42): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+34 more)

### Community 2 - "Community 2"
Cohesion: 0.07
Nodes (38): EstimateParams, _first_url(), GenerateImageParams, _Params, BaseModel, Generation tools on the platform's Agent API. Two of them, and the pair is the…, Find the produced file, whichever shape the reply uses. The catalogue documents…, Publish the generation tools. Call before ``registry.freeze()``. (+30 more)

### Community 3 - "Community 3"
Cohesion: 0.07
Nodes (23): Any, CommandFastPath, CommandPlanner, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim., Commands answered deterministically; everything else goes to a model. Ownership…, Maps one command to one tool call, then renders the result., Plan (+15 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (28): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+20 more)

### Community 5 - "Community 5"
Cohesion: 0.07
Nodes (27): BaseException, Completion, GenerationError, _has_result(), Any, VibemarketologSettings, Client for the platform's text generation endpoint. ``type=text`` is…, One synchronous text generation, recorded in the turn ledger. (+19 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (23): Agent, BindingTable, Message, bindings(), make_message(), The Telegram surface: who gets in, and whose tenant they act as., Distinct refusals would let someone probe which chats exist., The whole point of the boundary. (+15 more)

### Community 7 - "Community 7"
Cohesion: 0.08
Nodes (29): BaseSettings, Notified of every call the loop considered, with the guard's verdict. The point…, StepReporter, build_dispatcher(), BindingTable, Message, Telegram surface: resolve the conversation, then hand off to the agent. Replies…, Send one line per allowed call, before it runs. (+21 more)

### Community 8 - "Community 8"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (12): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., fixture, crm(), crm_registry(), ItmanoCrmSettings, Offline tests for the CRM adapter. Every response here comes from…, The planner sees descriptions and nothing else. (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.12
Nodes (15): Binding, BindingError, BindingTable, DenialReason, load_bindings(), Path, Which conversation may act for which tenant. This module is the authorization…, Decide whether this message may act, and for whom. (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.13
Nodes (16): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated(), test_an_unknown_lead_maps_to_not_found(), test_identity_matches_what_we_expect() (+8 more)

### Community 12 - "Community 12"
Cohesion: 0.14
Nodes (22): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+14 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (14): ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the…, contract_version(), load_contract(), Operation, operations(), Any (+6 more)

### Community 14 - "Community 14"
Cohesion: 0.12
Nodes (17): agent_tool_operations(), Any, ToolRegistry, Registration of the CRM tools into a :class:`ToolRegistry`. Descriptions here…, Operation ids the contract marks as belonging in an agent's catalogue.…, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register() (+9 more)

### Community 15 - "Community 15"
Cohesion: 0.21
Nodes (12): LlmPlanner, Turns a transcript plus a tool catalogue into the next step., mock, What a challenge page or a proxy error actually looks like., completion(), An unbounded repair loop is a hole in the cost ceiling., A 500 is not a parse problem; repeating the same prompt will not fix it., The safety net: if the model API is down, commands must still answer. (+4 more)

### Community 16 - "Community 16"
Cohesion: 0.15
Nodes (10): CrmError, _float_header(), _int_header(), Any, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift…, A call that did not succeed, already in CONDUIT's error vocabulary., Exception (+2 more)

### Community 17 - "Community 17"
Cohesion: 0.12
Nodes (12): AuditSink, Guard, Planner, Turns a transcript plus a tool catalogue into the next step., Deterministic-first gate in front of every call. Implementations run cheap…, Where action records go. The hash chain lives in the implementation., GuardStore, Record a write and return how many happened in the trailing hour. (+4 more)

### Community 18 - "Community 18"
Cohesion: 0.23
Nodes (5): parse(), Models wrap JSON in fences constantly, whatever the instructions say., Code catches this, not the model's good behaviour., A model adding commentary keys should not fail the whole plan., TestParsing

### Community 19 - "Community 19"
Cohesion: 0.26
Nodes (8): build_system_prompt(), One tool as the planner sees it: signature, purpose, per-argument notes. The…, _render_tool(), If the valid values are not in the prompt the model has to guess., Field descriptions used to be dropped from the prompt entirely. Only the tool-…, TestParameterNotesReachThePlanner, TestSystemPrompt, ToolSpec

### Community 20 - "Community 20"
Cohesion: 0.19
Nodes (10): _clip(), Trim only what is genuinely oversized, and say so when it happens. Silent…, planner(), The planner's parser, offline. Without native function calling the model…, A page of ten leads is ~3000 chars. Cutting it was the truncation bug., Silent truncation makes the model invent the rest or hedge blindly., settings(), TestNoParamsTool (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.20
Nodes (7): detect_language(), Name the language to answer in, or None when it is not clear. Deliberately…, PlanRequest, Decided in code, not left to a rule in a cached prompt. Three live failures…, leads' and 'en' occur in English too; a single hit proves nothing., A description saying "in English or Russian" seeded Russian replies to English…, TestReplyLanguage

### Community 22 - "Community 22"
Cohesion: 0.12
Nodes (9): LeadStage, parametrize, The catalogue documents several conventions. Look, do not guess., error_body(), Any, A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestErrorTranslation (+1 more)

### Community 23 - "Community 23"
Cohesion: 0.25
Nodes (8): _PlannedCall, _PlannerOutput, BaseModel, PlanRequest, A planner built on a text model that has no native function calling. The…, Strict. A near-miss is a failure, not something to bend into shape., _strip_fences(), _transcript()

### Community 24 - "Community 24"
Cohesion: 0.24
Nodes (8): CrmResponse, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, A successful call, plus the headers worth carrying forward., from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 25 - "Community 25"
Cohesion: 0.29
Nodes (3): Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 26 - "Community 26"
Cohesion: 0.25
Nodes (3): won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 28 - "Community 28"
Cohesion: 0.40
Nodes (3): AsyncClient, ItmanoCrmSettings, ToolErrorCode

### Community 30 - "Community 30"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **55 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ItmanoCrmClient` connect `Community 11` to `Community 5`, `Community 9`, `Community 13`, `Community 16`, `Community 24`, `Community 25`, `Community 28`?**
  _High betweenness centrality (0.041) - this node is a cross-community bridge._
- **Why does `InMemoryGuardStore` connect `Community 1` to `Community 4`?**
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