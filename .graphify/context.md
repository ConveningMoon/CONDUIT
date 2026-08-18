# Graph Report - .  (2026-08-18)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 878 nodes · 2087 edges · 61 communities (29 shown, 32 thin omitted)
- Extraction: 82% EXTRACTED · 18% INFERRED · 0% AMBIGUOUS · INFERRED: 368 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `af0cf6ad`
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

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 53 edges
2. `PlanRequest` - 45 edges
3. `Plan` - 42 edges
4. `InMemoryGuardStore` - 40 edges
5. `ToolContext` - 39 edges
6. `DeterministicGuard` - 37 edges
7. `Turn` - 34 edges
8. `CommandPlanner` - 34 edges
9. `Agent` - 33 edges
10. `ToolCall` - 32 edges

## Surprising Connections (you probably didn't know these)
- `ScriptedPlanner` --uses--> `PlanRequest`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `ScriptedPlanner` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `ExplodingPlanner` --uses--> `PlanRequest`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `ExplodingPlanner` --uses--> `Role`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py
- `RecordingAudit` --uses--> `PlanRequest`  [INFERRED]
  tests/test_agent.py → conduit/core/agent.py

## Import Cycles
- None detected.

## Communities (61 total, 32 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.05
Nodes (81): Agent, AuditEvent, AuditPhase, ExecutedCall, GuardDecision, Plan, BaseModel, Orchestration loop: intent, plan, guard, execute, report. The loop owns the… (+73 more)

### Community 1 - "Community 1"
Cohesion: 0.08
Nodes (40): DeterministicGuard, GuardRule, GuardSettings, InMemoryGuardStore, intent_hash(), ToolCall, ToolContext, ToolSpec (+32 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (40): EstimateParams, _first_url(), GenerateImageParams, _Params, Any, ToolRegistry, Generation tools on the platform's Agent API. Two of them, and the pair is the…, Find the produced file, whichever shape the reply uses. The catalogue documents… (+32 more)

### Community 3 - "Community 3"
Cohesion: 0.10
Nodes (28): AuditEvent, AuditRecord, AuditStore, ChainBreak, HashChainAuditSink, InMemoryAuditStore, Protocol, Tamper-evident action log. Each record carries the hash of the one before it,… (+20 more)

### Community 4 - "Community 4"
Cohesion: 0.06
Nodes (36): CreateEmailDraftParams, CreateLeadParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, LeadStage (+28 more)

### Community 5 - "Community 5"
Cohesion: 0.08
Nodes (21): BaseException, BaseSettings, Completion, GenerationError, _has_result(), Any, Client for the platform's text generation endpoint. ``type=text`` is…, Price and validate a generation without spending anything. Free, and the honest… (+13 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (16): LlmPlanner, completion(), parse(), mock, The planner's parser, offline. Without native function calling the model…, An unbounded repair loop is a hole in the cost ceiling., A 500 is not a parse problem; repeating the same prompt will not fix it., The safety net: if the model API is down, commands must still answer. (+8 more)

### Community 7 - "Community 7"
Cohesion: 0.10
Nodes (15): Path, BindingTable, fixture, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation. (+7 more)

### Community 8 - "Community 8"
Cohesion: 0.11
Nodes (16): Planner, PlanRequest, Turns a transcript plus a tool catalogue into the next step., What the planner is given. Deliberately model-agnostic., Role, CommandFastPath, Commands answered deterministically; everything else goes to a model. Ownership…, If the valid values are not in the prompt the model has to guess. (+8 more)

### Community 9 - "Community 9"
Cohesion: 0.15
Nodes (9): CommandPlanner, Any, ToolCall, Turn the tool result at the end of the transcript into a reply., Say what happened without repeating an upstream message verbatim., Maps one command to one tool call, then renders the result., _truncate(), Telegram sends /leads@thebot in groups. (+1 more)

### Community 10 - "Community 10"
Cohesion: 0.10
Nodes (21): Agent, BindingTable, Which conversation may act for which tenant. This module is the authorization…, build_dispatcher(), Telegram surface: resolve the conversation, then hand off to the agent. Replies…, Long-poll for updates. Deployment swaps this for a webhook., run(), Telegram interface: session to tenant mapping, and the command fast path. (+13 more)

### Community 11 - "Community 11"
Cohesion: 0.10
Nodes (20): Any, agent_tool_operations(), Any, ToolRegistry, Registration of the CRM tools into a :class:`ToolRegistry`. Descriptions here…, Operation ids the contract marks as belonging in an agent's catalogue.…, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The… (+12 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (11): mock, parametrize, error_body(), Any, If this ever stops being null the tool description is a lie., What a challenge page or a proxy error actually looks like., The contract really does declare 201 here, not 200., TestErrorTranslation (+3 more)

### Community 13 - "Community 13"
Cohesion: 0.12
Nodes (17): CrmError, CrmResponse, _float_header(), _int_header(), Any, HTTP client for the CRM agent surface. Failures raise :class:`CrmError`…, Perform one operation from the contract., Download the contract the server is publishing right now. Used to detect drift… (+9 more)

### Community 14 - "Community 14"
Cohesion: 0.11
Nodes (15): AgentReply, AuditSink, Guard, NullAuditSink, ToolCall, ToolContext, ToolSpec, Deterministic-first gate in front of every call. Implementations run cheap… (+7 more)

### Community 15 - "Community 15"
Cohesion: 0.13
Nodes (17): current_ledger(), ModelCall, Per-turn ledger of model calls. Cost and model choice are decisions this system…, One request to a language model, and what it cost., Collect every model call made inside this block., Add to the ledger if one is open. A no-op otherwise, never an error., record_model_call(), turn_ledger() (+9 more)

### Community 16 - "Community 16"
Cohesion: 0.12
Nodes (14): ItmanoCrmSettings, Configuration for the ITMANO CRM adapter. Everything arrives via env vars., Connection details plus the assertion that guards against pointing here at the…, contract_version(), load_contract(), Operation, operations(), Any (+6 more)

### Community 17 - "Community 17"
Cohesion: 0.15
Nodes (12): ConfigurationError, The adapter is pointed somewhere it was not meant to reach., fixture, crm(), crm_registry(), ItmanoCrmSettings, Offline tests for the CRM adapter. Every response here comes from…, The planner sees descriptions and nothing else. (+4 more)

### Community 18 - "Community 18"
Cohesion: 0.15
Nodes (15): ItmanoCrmClient, One client per process. Holds the connection pool; owns no state., client(), Live checks against the CRM sandbox. Read-only, and skipped by default. These…, Drift detector. The vendored contract is where per-operation timeouts and the…, test_an_over_large_limit_is_rejected_not_truncated(), test_an_unknown_lead_maps_to_not_found(), test_identity_matches_what_we_expect() (+7 more)

### Community 19 - "Community 19"
Cohesion: 0.15
Nodes (17): build_system_prompt(), _clip(), LlmPlanner, _PlannedCall, _PlannerOutput, BaseModel, PlanRequest, A planner built on a text model that has no native function calling. The… (+9 more)

### Community 20 - "Community 20"
Cohesion: 0.22
Nodes (12): Turns a Telegram message into an agent turn, or refuses it., TelegramGateway, make_message(), BindingTable, Message, parametrize, Distinct refusals would let someone probe which chats exist., The whole point of the boundary. (+4 more)

### Community 21 - "Community 21"
Cohesion: 0.18
Nodes (8): Send one line per allowed call, before it runs., Keep the 'typing' state alive while the turn runs., What the last turn cost, and on which model. Model choice is a decision made on…, Record enough to write a binding, and nothing the sender said. The chat id is…, Message, Resolution, StepReporter, Task

### Community 22 - "Community 22"
Cohesion: 0.20
Nodes (6): GuardStore, Protocol, Record a write and return how many happened in the trailing hour., Record an intent and return how often it occurred inside the window., Counters and switches the rules read and write. Deliberately narrow, and every…, Record a call in this turn and return the running count, this one included.

### Community 23 - "Community 23"
Cohesion: 0.25
Nodes (4): BaseModel, Refuse to serve anything if the server is not who we expect. Called once before…, Identity the server reports for our token., WhoAmI

### Community 24 - "Community 24"
Cohesion: 0.25
Nodes (4): LeadStage, A rejected enum costs a whole extra planning round trip, so accept the English…, Normalising is not the same as accepting anything., TestStageAliases

### Community 25 - "Community 25"
Cohesion: 0.25
Nodes (3): won' used to be the example here; it is now a recognised alias for 'cerrado',…, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 26 - "Community 26"
Cohesion: 0.39
Nodes (3): The 80-second wait is only bearable if it is announced., An expected wait is patience; an unexplained one reads as a crash., TestStepDescriptions

### Community 27 - "Community 27"
Cohesion: 0.40
Nodes (3): AsyncClient, ItmanoCrmSettings, ToolErrorCode

### Community 28 - "Community 28"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **32 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 0` to `Community 11`?**
  _High betweenness centrality (0.049) - this node is a cross-community bridge._
- **Why does `ItmanoCrmClient` connect `Community 18` to `Community 5`, `Community 12`, `Community 13`, `Community 16`, `Community 17`, `Community 23`, `Community 27`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **Why does `PlanRequest` connect `Community 8` to `Community 0`, `Community 4`, `Community 6`, `Community 9`, `Community 10`, `Community 14`, `Community 20`, `Community 26`?**
  _High betweenness centrality (0.042) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `ToolRegistry` (e.g. with `EchoParams` and `NoParams`) actually correct?**
  _`ToolRegistry` has 14 INFERRED edges - model-reasoned connections that need verification._
- **Are the 24 inferred relationships involving `PlanRequest` (e.g. with `CommandFastPath` and `CommandPlanner`) actually correct?**
  _`PlanRequest` has 24 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Plan` (e.g. with `CommandFastPath` and `CommandPlanner`) actually correct?**
  _`Plan` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `InMemoryGuardStore` (e.g. with `TestChaining` and `TestTampering`) actually correct?**
  _`InMemoryGuardStore` has 10 INFERRED edges - model-reasoned connections that need verification._