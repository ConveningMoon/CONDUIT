# Graph Report - .  (2026-08-17)

## Corpus Check
- cluster-only mode — file stats not available

## Summary
- 491 nodes · 1404 edges · 26 communities (19 shown, 7 thin omitted)
- Extraction: 73% EXTRACTED · 27% INFERRED · 0% AMBIGUOUS · INFERRED: 384 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `d15f0bcc`
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

## God Nodes (most connected - your core abstractions)
1. `ToolRegistry` - 70 edges
2. `ToolContext` - 61 edges
3. `ToolCall` - 53 edges
4. `ToolSpec` - 46 edges
5. `ToolResult` - 44 edges
6. `SideEffect` - 39 edges
7. `BindingTable` - 38 edges
8. `ToolStatus` - 34 edges
9. `Plan` - 33 edges
10. `Agent` - 31 edges

## Surprising Connections (you probably didn't know these)
- `EchoParams` --uses--> `SideEffect`  [INFERRED]
  tests/conftest.py → conduit/core/tools.py
- `NoParams` --uses--> `SideEffect`  [INFERRED]
  tests/conftest.py → conduit/core/tools.py
- `TestInvoke` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py
- `TestRegistry` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py
- `TestResultEnvelope` --uses--> `SideEffect`  [INFERRED]
  tests/test_tools.py → conduit/core/tools.py

## Import Cycles
- None detected.

## Communities (26 total, 7 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.11
Nodes (59): Agent, AgentReply, AuditEvent, AuditPhase, AuditSink, ExecutedCall, Guard, GuardDecision (+51 more)

### Community 1 - "Community 1"
Cohesion: 0.05
Nodes (48): AsyncClient, BaseException, BaseModel, ConfigurationError, CrmError, CrmResponse, _float_header(), _int_header() (+40 more)

### Community 2 - "Community 2"
Cohesion: 0.06
Nodes (35): DuplicateToolError, Protocol, Tool registry and calling protocol. This module is the contract every other…, The shape of a tool implementation., Raised when two tools claim the same name., Raised when a name is looked up that was never registered., Raised on an attempt to register after the registry was frozen., Name-to-implementation map, populated at startup and then frozen. Freezing… (+27 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (17): Any, Argument schema, in the form a function-calling planner expects., Every spec, or only those of one adapter, sorted by name., What the planner is shown., CommandPlanner, Plan, PlanRequest, Turn the tool result at the end of the transcript into a reply. (+9 more)

### Community 4 - "Community 4"
Cohesion: 0.14
Nodes (10): mock, parametrize, error_body(), Any, If this ever stops being null the tool description is a lie., What a challenge page or a proxy error actually looks like., The contract really does declare 201 here, not 200., TestErrorTranslation (+2 more)

### Community 5 - "Community 5"
Cohesion: 0.16
Nodes (8): BindingTable, Immutable lookup from chat to tenant. Deliberately offers no way to add, remove…, Knowing the chat is not the same as being allowed to speak in it., The binding was written for a private conversation., There must be no way to read a tenant off a refusal., No command, no onboarding flow, no setter. Deployment only., TestImmutability, TestResolution

### Community 6 - "Community 6"
Cohesion: 0.18
Nodes (11): Message, Turns a Telegram message into an agent turn, or refuses it., Record enough to write a binding, and nothing the sender said. The chat id is…, TelegramGateway, make_message(), Message, Distinct refusals would let someone probe which chats exist., The whole point of the boundary. (+3 more)

### Community 7 - "Community 7"
Cohesion: 0.23
Nodes (16): CreateEmailDraftParams, CreateNoteParams, GetDealParams, GetLeadParams, Intent, Language, ListDealsParams, NoParams (+8 more)

### Community 8 - "Community 8"
Cohesion: 0.26
Nodes (9): load_bindings(), Path, Read the binding file. Any doubt is fatal rather than permissive., Path, The authorization boundary of the messaging surface. These are the tests that…, Starting with zero bindings denies everything, but it is a mistake., Two tenants claiming one chat is not something to resolve by ordering., TestLoading (+1 more)

### Community 9 - "Community 9"
Cohesion: 0.21
Nodes (12): BaseSettings, build_dispatcher(), Agent, Telegram surface: resolve the conversation, then hand off to the agent. Replies…, Long-poll for updates. Deployment swaps this for a webhook., run(), Configuration for the Telegram interface., TelegramSettings (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.17
Nodes (8): BindingError, DenialReason, Which conversation may act for which tenant. This module is the authorization…, Decide whether this message may act, and for whom., The binding file is unusable. Always fatal: never start without it., Outcome of resolving one incoming message., Resolution, RuntimeError

### Community 11 - "Community 11"
Cohesion: 0.16
Nodes (8): LeadStage, Funnel stage. Moved by a person, never by the system., agent_tool_operations(), Operation ids the contract marks as belonging in an agent's catalogue.…, ToolRegistry, The planner sees descriptions and nothing else., TestContract, TestRegistration

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (13): Binding, One conversation, bound to one tenant., A deterministic planner for explicit commands. CONDUIT's orchestration loop…, fixture, table(), bindings(), Agent, fixture (+5 more)

### Community 13 - "Community 13"
Cohesion: 0.24
Nodes (9): fixture, ItmanoCrmSettings, ctx(), crm(), crm_registry(), ItmanoCrmClient, Offline tests for the CRM adapter. Every response here comes from…, settings() (+1 more)

### Community 14 - "Community 14"
Cohesion: 0.24
Nodes (10): Any, ItmanoCrmClient, ToolRegistry, Perform a call and flatten every expected failure into a result., Publish the CRM tools. Call once at startup, before ``registry.freeze()``. The…, register(), _run(), _spec() (+2 more)

### Community 15 - "Community 15"
Cohesion: 0.33
Nodes (4): CreateLeadParams, ListLeadsParams, The CRM has no unassigned state, so this must never reach the network., TestArgumentValidation

### Community 16 - "Community 16"
Cohesion: 0.47
Nodes (5): from_code(), from_status(), ToolErrorCode, Translation from the CRM's error vocabulary into CONDUIT's. The CRM publishes a…, Map a published error code. Falls back to the status when unrecognised. An…

### Community 17 - "Community 17"
Cohesion: 0.53
Nodes (5): main(), percentile(), Measure what a CRM tool call actually costs, through the real invocation path.…, timed(), ToolRegistry

### Community 18 - "Community 18"
Cohesion: 0.67
Nodes (3): _imported_modules(), Executable form of the dependency rule: the core points inward only., test_core_never_imports_adapters_or_interfaces()

## Knowledge Gaps
- **1 isolated node(s):** `conduit`
  These have ≤1 connection - possible missing edges or undocumented components.
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `ToolRegistry` connect `Community 2` to `Community 0`, `Community 3`?**
  _High betweenness centrality (0.102) - this node is a cross-community bridge._
- **Why does `BindingTable` connect `Community 5` to `Community 3`, `Community 6`, `Community 8`, `Community 9`, `Community 10`, `Community 12`?**
  _High betweenness centrality (0.093) - this node is a cross-community bridge._
- **Why does `CommandPlanner` connect `Community 3` to `Community 9`, `Community 12`, `Community 6`?**
  _High betweenness centrality (0.086) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `ToolRegistry` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolRegistry` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 30 inferred relationships involving `ToolContext` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolContext` has 30 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolCall` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolCall` has 28 INFERRED edges - model-reasoned connections that need verification._
- **Are the 28 inferred relationships involving `ToolSpec` (e.g. with `Agent` and `AgentReply`) actually correct?**
  _`ToolSpec` has 28 INFERRED edges - model-reasoned connections that need verification._