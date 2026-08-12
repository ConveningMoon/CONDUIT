# CONDUIT

Conversational agent layer between a messaging interface and business systems.

A user talks to a Telegram bot. CONDUIT understands the request, decides which
tools to call, enforces limits before acting, executes against a business system,
and reports back — with memory, cost control, and a tamper-evident audit trail.

Two adapters ship with it:

- `itmano_crm` — leads, contacts, deals, email drafting against a multi-tenant CRM
- `vibemarketolog` — content generation via a third-party Agent API

The core knows nothing about either.

## Layout

```
conduit/
  core/         provider-agnostic orchestration, guard, audit, memory, cost
  adapters/     one package per business system
  interfaces/   one package per messaging surface
  demo_data/    synthetic tenant, fabricated records only
tests/
migrations/
```

Dependencies point inward. `core/` never imports from `adapters/` or `interfaces/`.

## Development

```bash
py -3.12 -m venv .venv
.venv\Scripts\activate            # PowerShell: .venv\Scripts\Activate.ps1
pip install -e ".[dev]"
cp .env.example .env              # then fill it in
```

Checks that must pass before any commit:

```bash
ruff check .
ruff format --check .
mypy conduit
pytest
```

## Status

Early. The tool-calling protocol and the orchestration loop are in place and
tested. No adapter is wired yet, and the default guard denies every write.
