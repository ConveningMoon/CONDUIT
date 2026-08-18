# Graph Report - .  (2026-08-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 892 nodes · 2058 edges · 72 communities (33 shown, 39 thin omitted)
- Extraction: 84% EXTRACTED · 16% INFERRED · 0% AMBIGUOUS · INFERRED: 324 edges (avg confidence: 0.52)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `746bc23a`
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

## Communities (72 total, 39 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (85): Agent, AgentReply, AuditEvent, AuditPhase, GuardDecision, Plan, Planner, PlanRequest (+77 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (43): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+35 more)

### Community 2 - "Community 2"
Cohesion: 0.05
Nodes (43): build_system_prompt(), _clip(), LlmPlanner, Plan, PlanRequest, ToolSpec, Trim only what is genuinely oversized, and say so when it happens. Silent…, Turns a transcript plus a tool catalogue into the next step. (+35 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (41): BaseException, BaseSettings, Completion, GenerationError, _has_result(), Any, VibemarketologSettings, Client for the platform's text generation endpoint. ``type=text`` is… (+33 more)

### Community 4 - "Community 4"
Cohesion: 0.10
Nodes (26): _first_url(), GenerateImageParams, Any, Find the produced file, whichever shape the reply uses. The catalogue documents…, mock_candidate_prices(), mock, ToolRegistry, Generation tools, offline. Every response here is simulated. Real generation… (+18 more)

### Community 5 - "Community 5"
Cohesion: 0.11
Nodes (25): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+17 more)

### Community 6 - "Community 6"
Cohesion: 0.08
Nodes (26): Any, agent_tool_operations(), Any, ToolRegistry, Registration of the CRM tools into a :class:`ToolRegistry`. Descriptions here…, Operation ids the contract marks as belonging in an agent's catalogue.…, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The… (+18 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 8 - "Community 8"
Cohesion: 0.12
Nodes (12): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., mock, If this ever stops being null the tool description is a lie., The contract really does declare 201 here, not 200., The failure that actually happens at startup is a transient challenge from the…, A bad token is a definite answer. Repeating it just wastes startup., Retrying must not soften the check it exists for. (+4 more)

### Community 9 - "Community 9"
Cohesion: 0.14
Nodes (22): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+14 more)

### Community 10 - "Community 10"
Cohesion: 0.13
Nodes (15): AuditSink, ExecutedCall, Guard, NullAuditSink, ToolCall, ToolContext, ToolSpec, Deterministic-first gate in front of every call. Implementations run cheap… (+7 more)

### Community 11 - "Community 11"
Cohesion: 0.12
Nodes (14): Binding, BindingError, BindingTable, DenialReason, load_bindings(), Path, Decide whether this message may act, and for whom., Read the binding file. Any doubt is fatal rather than permissive. (+6 more)

### Community 12 - "Community 12"
Cohesion: 0.13
Nodes (15): CrmResponse, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, A successful call, plus the headers worth carrying forward., Configuration for the ITMANO CRM adapter. Everything arrives via env vars., contract_version(), load_contract(), Operation, operations() (+7 more)

### Community 13 - "Community 13"
Cohesion: 0.20
Nodes (10): BindingTable, bindings(), make_message(), The Telegram surface: who gets in, and whose tenant they act as., Distinct refusals would let someone probe which chats exist., The whole point of the boundary., Narration must never be able to kill what it narrates., TestAuthorisation (+2 more)

### Community 14 - "Community 14"
Cohesion: 0.15
Nodes (10): CrmError, _float_header(), _int_header(), Any, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift…, A call that did not succeed, already in CONDUIT's error vocabulary., Exception (+2 more)

### Community 15 - "Community 15"
Cohesion: 0.16
Nodes (13): Send one line per allowed call, before it runs., Keep the 'typing' state alive while the turn runs., What the last turn cost, and on which model. Model choice is a decision made on…, Record enough to write a binding, and nothing the sender said. The chat id is…, Long-poll for updates. Deployment swaps this for a webhook., Turns a Telegram message into an agent turn, or refuses it., run(), TelegramGateway (+5 more)

### Community 16 - "Community 16"
Cohesion: 0.17
Nodes (11): Which conversation may act for which tenant. This module is the authorization…, build_dispatcher(), Telegram surface: resolve the conversation, then hand off to the agent. Replies…, Configuration for the Telegram interface., Telegram interface: session to tenant mapping, and the command fast path., describe_step(), ToolSpec, A deterministic planner for explicit commands. CONDUIT's orchestration loop… (+3 more)

### Community 17 - "Community 17"
Cohesion: 0.28
Nodes (6): CommandPlanner, Maps one command to one tool call, then renders the result., Plan, PlanRequest, Telegram sends /leads@thebot in groups., TestCommandPlanner

### Community 18 - "Community 18"
Cohesion: 0.17
Nodes (8): main(), percentile(), Measure what a CRM tool call actually costs, through the real invocation path.…, timed(), The planner sees descriptions and nothing else., TestContract, TestRegistration, ToolRegistry

### Community 19 - "Community 19"
Cohesion: 0.21
Nodes (13): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., ItmanoCrmSettings, Connection details plus the assertion that guards against pointing here at the…, client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated() (+5 more)

### Community 20 - "Community 20"
Cohesion: 0.19
Nodes (10): fixture, crm(), crm_registry(), error_body(), Any, ItmanoCrmSettings, Offline tests for the CRM adapter. Every response here comes from…, What a challenge page or a proxy error actually looks like. (+2 more)

### Community 21 - "Community 21"
Cohesion: 0.17
Nodes (6): LeadStage, parametrize, The catalogue documents several conventions. Look, do not guess., A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestStageAliases

### Community 22 - "Community 22"
Cohesion: 0.20
Nodes (6): GuardStore, Protocol, Record a write and return how many happened in the trailing hour., Record an intent and return how often it occurred inside the window., Counters and switches the rules read and write. Deliberately narrow, and every…, Record a call in this turn and return the running count, this one included.

### Community 23 - "Community 23"
Cohesion: 0.29
Nodes (3): Any, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim.

### Community 24 - "Community 24"
Cohesion: 0.25
Nodes (4): BaseModel, Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 25 - "Community 25"
Cohesion: 0.39
Nodes (4): CommandFastPath, Plan, PlanRequest, Commands answered deterministically; everything else goes to a model. Ownership…

### Community 26 - "Community 26"
Cohesion: 0.25
Nodes (3): won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 27 - "Community 27"
Cohesion: 0.39
Nodes (3): The 80-second wait is only bearable if it is announced., An expected wait is patience; an unexplained one reads as a crash. A range, not…, TestStepDescriptions

### Community 28 - "Community 28"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 29 - "Community 29"
Cohesion: 0.47
Nodes (3): Plain text, no parse mode. The demo tenant seeds exactly this case., A missing number is a number the reader invents., TestRendering

### Community 30 - "Community 30"
Cohesion: 0.40
Nodes (3): AsyncClient, ItmanoCrmSettings, ToolErrorCode

### Community 31 - "Community 31"
Cohesion: 0.50
Nodes (4): Agent, Always calls the spy tool, then reports what it saw., spy_agent(), SpyTenantPlanner

### Community 32 - "Community 32"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **39 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 0` to `Community 6`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `CommandPlanner` connect `Community 17` to `Community 13`, `Community 16`, `Community 23`, `Community 25`, `Community 27`, `Community 29`, `Community 31`?**
  _High betweenness centrality (0.046) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 19` to `Community 3`, `Community 8`, `Community 12`, `Community 14`, `Community 20`, `Community 24`, `Community 30`?**
  _High betweenness centrality (0.040) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ToolRegistry` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolRegistry` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `InMemoryGuardStore` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`InMemoryGuardStore` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 14 inferred relationships involving `ToolContext` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolContext` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `DeterministicGuard` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`DeterministicGuard` has 10 INFERRED edges - model-reasoned connections that need verification._