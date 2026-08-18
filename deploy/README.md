# Deploying the bot on a VPS

The bot long-polls Telegram, so **it needs no inbound port**. Do not open the
firewall and do not migrate to webhooks: polling is what keeps this deployment
free of an attack surface.

**One instance only.** The guard's ceilings and the audit chain live in process
memory, so a second replica would keep its own counters and neither would be a
ceiling. Scaling out means moving `GuardStore` to Redis first.

## Prerequisites

**Python 3.12 or newer**, and the requirement is real rather than aspirational:
`core/tools.py` declares generics with PEP 695 syntax, which 3.11 cannot parse,
and `StrEnum`, `asyncio.timeout`, `datetime.UTC` and `tomllib` all need 3.11.

Check what the machine has before installing anything:

    python3 --version
    head -2 /etc/os-release

Ubuntu 22.04 ships 3.10, so it needs a newer interpreter alongside the system
one. **Never replace the system python3** — apt and other services depend on it.

## Install

    sudo useradd --system --home-dir /opt/conduit --shell /usr/sbin/nologin conduit
    sudo mkdir -p /opt/conduit && sudo chown conduit:conduit /opt/conduit
    sudo -u conduit git clone https://github.com/ConveningMoon/CONDUIT.git /opt/conduit
    cd /opt/conduit
    sudo -u conduit git checkout feat/itmano-crm-adapter

Note the missing `--create-home`: `useradd` would populate the directory with
skeleton files, and `git clone` refuses a directory that is not empty.

### Python 3.12, contained (preferred on a shared machine)

Installs a standalone interpreter under the service account. Nothing
system-wide changes, which matters when the box runs something else that people
depend on.

    sudo -u conduit bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
    sudo -u conduit /opt/conduit/.local/bin/uv python install 3.12
    sudo -u conduit /opt/conduit/.local/bin/uv venv --python 3.12 /opt/conduit/.venv
    sudo -u conduit /opt/conduit/.local/bin/uv pip install --python /opt/conduit/.venv/bin/python -e /opt/conduit

### Python 3.12, from apt

Adds a third-party archive to the whole system. Fine on a dedicated box, more
than is needed on a shared one.

    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update && sudo apt install -y python3.12 python3.12-venv
    sudo -u conduit python3.12 -m venv /opt/conduit/.venv
    sudo -u conduit /opt/conduit/.venv/bin/pip install -e /opt/conduit

Either way the interpreter ends up at `/opt/conduit/.venv/bin/python`, which is
what the systemd unit runs.

### Verify before going further

    sudo -u conduit /opt/conduit/.venv/bin/python -c "import sys, conduit; print(sys.version)"

## Configure

Two files, neither of which is in the repository.

`/opt/conduit/.env` — carries both API tokens, so it is readable by nobody else:

    sudo -u conduit tee /opt/conduit/.env >/dev/null <<'ENV'
    ...contents...
    ENV
    sudo chmod 600 /opt/conduit/.env

`/opt/conduit/config/telegram_bindings.toml` — the authorization boundary. It
decides which conversation may act for which tenant, and nothing inside a chat
can change it.

    sudo chmod 600 /opt/conduit/config/telegram_bindings.toml

## Run

    sudo cp /opt/conduit/deploy/conduit-bot.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable --now conduit-bot
    sudo systemctl status conduit-bot --no-pager

A healthy start logs, in order: `bindings.loaded`, `crm.verified`,
`tools.registered count=13`, `planner.ready`, then `Run polling`.

`crm.unavailable` instead of `crm.verified` means the CRM could not be reached
and **its 11 tools were not registered**. The bot still answers, with generation
only. That is deliberate, but it is not what you want during a demo — restart and
check again.

## Logs

    sudo journalctl -u conduit-bot -f
    sudo journalctl -u conduit-bot --since "10 minutes ago" --no-pager

Cap the journal so an error loop cannot fill the disk:

    sudo mkdir -p /etc/systemd/journald.conf.d
    printf '[Journal]\nSystemMaxUse=500M\n' | sudo tee /etc/systemd/journald.conf.d/size.conf
    sudo systemctl restart systemd-journald

## Updating

    cd /opt/conduit
    sudo -u conduit git pull
    sudo -u conduit .venv/bin/pip install -e .
    sudo systemctl restart conduit-bot
