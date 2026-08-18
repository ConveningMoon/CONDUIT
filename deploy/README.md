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

The repository lives in a subdirectory of the account's home, and the venv sits
next to it rather than inside it — kept separate so an interpreter upgrade never
means touching the checkout.

    sudo useradd --system --create-home --home-dir /opt/conduit --shell /usr/sbin/nologin conduit
    sudo -u conduit git clone https://github.com/ConveningMoon/CONDUIT.git /opt/conduit/CONDUIT
    cd /opt/conduit/CONDUIT
    sudo -u conduit git checkout feat/itmano-crm-adapter

Every path below follows from this layout: the repo at `/opt/conduit/CONDUIT`,
the interpreter at `/opt/conduit/.venv`.

### Python 3.12, contained (preferred on a shared machine)

Installs a standalone interpreter under the service account. Nothing
system-wide changes, which matters when the box runs something else that people
depend on.

    sudo -u conduit bash -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
    sudo -u conduit /opt/conduit/.local/bin/uv python install 3.12
    sudo -u conduit /opt/conduit/.local/bin/uv venv --python 3.12 /opt/conduit/.venv
    sudo -u conduit /opt/conduit/.local/bin/uv pip install --python /opt/conduit/.venv/bin/python -e /opt/conduit/CONDUIT

### Python 3.12, from apt

Adds a third-party archive to the whole system. Fine on a dedicated box, more
than is needed on a shared one.

    sudo add-apt-repository -y ppa:deadsnakes/ppa
    sudo apt update && sudo apt install -y python3.12 python3.12-venv
    sudo -u conduit python3.12 -m venv /opt/conduit/.venv
    sudo -u conduit /opt/conduit/.venv/bin/pip install -e /opt/conduit/CONDUIT

Either way the interpreter ends up at `/opt/conduit/.venv/bin/python`, which is
what the systemd unit runs.

### Verify before going further

    cd /opt/conduit/CONDUIT
    sudo -u conduit /opt/conduit/.venv/bin/python -c "import sys, conduit; print(sys.version)"

`import conduit` only works from inside the checkout in editable-install mode, so
run it from `/opt/conduit/CONDUIT` as shown, not from the home directory.

## Configure

Two files, neither of which is in the repository.

`/opt/conduit/CONDUIT/.env` — carries both API tokens, so it is readable by
nobody else. Copy it from the laptop rather than retyping it:

    scp .env conduit-vps:/tmp/conduit.env
    # on the VPS:
    sudo mv /tmp/conduit.env /opt/conduit/CONDUIT/.env
    sudo chown conduit:conduit /opt/conduit/CONDUIT/.env
    sudo chmod 600 /opt/conduit/CONDUIT/.env

`/opt/conduit/CONDUIT/config/telegram_bindings.toml` — the authorization
boundary. It decides which conversation may act for which tenant, and nothing
inside a chat can change it.

    scp config/telegram_bindings.toml conduit-vps:/tmp/bindings.toml
    # on the VPS:
    sudo mv /tmp/bindings.toml /opt/conduit/CONDUIT/config/telegram_bindings.toml
    sudo chown conduit:conduit /opt/conduit/CONDUIT/config/telegram_bindings.toml
    sudo chmod 600 /opt/conduit/CONDUIT/config/telegram_bindings.toml

## Run

    sudo cp /opt/conduit/CONDUIT/deploy/conduit-bot.service /etc/systemd/system/
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

    cd /opt/conduit/CONDUIT
    sudo -u conduit git pull
    sudo -u conduit /opt/conduit/.venv/bin/pip install -e .
    sudo systemctl restart conduit-bot
