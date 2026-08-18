# Deploying the bot on a VPS

The bot long-polls Telegram, so **it needs no inbound port**. Do not open the
firewall and do not migrate to webhooks: polling is what keeps this deployment
free of an attack surface.

**One instance only.** The guard's ceilings and the audit chain live in process
memory, so a second replica would keep its own counters and neither would be a
ceiling. Scaling out means moving `GuardStore` to Redis first.

## Prerequisites

Python 3.12 or newer. Check before installing anything:

    python3 --version
    cat /etc/os-release | head -2

## Install

    sudo useradd --system --create-home --home-dir /opt/conduit --shell /usr/sbin/nologin conduit
    sudo -u conduit git clone https://github.com/ConveningMoon/CONDUIT.git /opt/conduit
    cd /opt/conduit
    sudo -u conduit git checkout feat/itmano-crm-adapter
    sudo -u conduit python3 -m venv .venv
    sudo -u conduit .venv/bin/pip install -e .

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
