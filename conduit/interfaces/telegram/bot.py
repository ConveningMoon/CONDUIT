"""Telegram surface: resolve the conversation, then hand off to the agent.

Replies are sent as plain text with no parse mode. The demo tenant deliberately
contains a surname with an apostrophe and others with accents, and Markdown
escaping is a reliable source of either mangled names or failed sends. Plain text
has neither failure mode.
"""

from __future__ import annotations

import asyncio
import contextlib
import uuid
from dataclasses import dataclass, field

import structlog
from aiogram import Bot, Dispatcher
from aiogram.types import Message

from conduit.core.agent import Agent, GuardDecision, StepReporter
from conduit.core.telemetry import ModelCall, turn_ledger
from conduit.core.tools import ToolCall, ToolContext, ToolSpec
from conduit.interfaces.telegram.bindings import BindingTable, Resolution
from conduit.interfaces.telegram.config import TelegramSettings
from conduit.interfaces.telegram.planner import describe_step

__all__ = ["REFUSAL", "TYPING_REFRESH_SECONDS", "TelegramGateway", "build_dispatcher"]

TYPING_REFRESH_SECONDS = 4.0
"""Telegram drops the typing state after about five seconds, so it has to be
re-sent while the model thinks. Sending it once at the start would let the
silence reappear at exactly the point the wait feels longest."""

log = structlog.get_logger(__name__)

REFUSAL = "This conversation is not authorised to use this bot."
"""One refusal for every reason.

Distinct messages would let someone probing the bot tell an unknown chat from a
known chat they are not allowed to speak in. Same shape as the CRM answering 404
rather than 403 for another tenant's record.
"""

PROBLEM = "Something went wrong handling that. It has been logged."


@dataclass(slots=True)
class TelegramGateway:
    """Turns a Telegram message into an agent turn, or refuses it."""

    agent: Agent
    bindings: BindingTable
    show_steps: bool = True
    last_turn: dict[str, list[ModelCall]] = field(default_factory=dict)
    """Model calls from the most recent turn of each session, for ``/debug``.
    One entry per conversation, overwritten each turn — a log, not a ledger."""

    async def handle(self, message: Message) -> str:
        chat = message.chat
        sender = message.from_user
        text = (message.text or "").strip()

        if sender is None or not text:
            return REFUSAL

        resolution = self.bindings.resolve(
            chat_id=chat.id,
            user_id=sender.id,
            is_private=chat.type == "private",
        )
        if not resolution.allowed:
            self._log_denial(resolution, chat_id=chat.id, user_id=sender.id)
            return REFUSAL

        binding = resolution.binding
        assert binding is not None  # narrowed by resolution.allowed

        session_id = f"telegram:{chat.id}"

        if text.split()[0].lstrip("/").split("@", 1)[0].lower() == "debug":
            return self._debug(session_id)

        ctx = ToolContext(
            tenant_id=binding.tenant_id,
            session_id=session_id,
            actor_id=f"telegram:{sender.id}",
            request_id=uuid.uuid4().hex,
            idempotency_key=f"tg-{chat.id}-{message.message_id}",
        )

        typing = self._start_typing(message)
        self.agent.on_step = self._reporter(message) if self.show_steps else None
        try:
            with turn_ledger() as ledger:
                reply = await self.agent.run(text, ctx)
            self.last_turn[session_id] = ledger
        # The interface is the last line: a crash here is a silent bot.
        except Exception:
            log.exception(
                "telegram.turn_failed",
                tenant_id=binding.tenant_id,
                session_id=session_id,
                request_id=ctx.request_id,
            )
            return PROBLEM
        finally:
            if typing is not None:
                typing.cancel()

        log.info(
            "telegram.turn",
            tenant_id=binding.tenant_id,
            session_id=session_id,
            request_id=ctx.request_id,
            stop_reason=reply.stop_reason.value,
            calls=len(reply.calls),
            model_calls=len(ledger),
            cost_rub=round(sum(entry.cost_rub for entry in ledger), 3),
        )
        return reply.text or PROBLEM

    def _reporter(self, message: Message) -> StepReporter | None:
        """Send one line per allowed call, before it runs."""
        bot = message.bot
        if bot is None:
            return None

        async def report(call: ToolCall, spec: ToolSpec, decision: GuardDecision) -> None:
            await bot.send_message(message.chat.id, describe_step(call, spec, decision))

        return report

    @staticmethod
    def _start_typing(message: Message) -> asyncio.Task[None] | None:
        """Keep the 'typing' state alive while the turn runs."""
        bot = message.bot
        if bot is None:
            return None

        async def loop() -> None:
            with contextlib.suppress(asyncio.CancelledError, Exception):
                while True:
                    await bot.send_chat_action(message.chat.id, "typing")
                    await asyncio.sleep(TYPING_REFRESH_SECONDS)

        return asyncio.create_task(loop())

    def _debug(self, session_id: str) -> str:
        """What the last turn cost, and on which model.

        Model choice is a decision made on the user's behalf; leaving it in a
        config file means nobody can check whether the cheap one was right.
        """
        entries = self.last_turn.get(session_id)
        if not entries:
            return "No model calls yet this session. Commands are answered without one."

        lines = [
            f"• {entry.model}  {entry.cost_rub:.2f} RUB  {entry.latency_ms} ms"
            f"  in/out {entry.input_tokens}/{entry.output_tokens}"
            + (f"  cached {entry.cached_tokens}" if entry.cached_tokens else "")
            + ("  (retry after an unparseable reply)" if entry.retry else "")
            for entry in entries
        ]
        total = sum(entry.cost_rub for entry in entries)
        return f"Last turn: {len(entries)} model call(s), {total:.2f} RUB total\n" + "\n".join(
            lines
        )

    @staticmethod
    def _log_denial(resolution: Resolution, *, chat_id: int, user_id: int) -> None:
        """Record enough to write a binding, and nothing the sender said.

        The chat id is here on purpose: it is how an operator learns the value to
        put in the binding file, without anyone having to guess it.
        """
        log.warning(
            "telegram.denied",
            reason=resolution.reason.value if resolution.reason else "unknown",
            chat_id=chat_id,
            user_id=user_id,
        )


def build_dispatcher(gateway: TelegramGateway) -> Dispatcher:
    dispatcher = Dispatcher()

    @dispatcher.message()
    async def on_message(message: Message) -> None:
        await message.answer(await gateway.handle(message))

    return dispatcher


CONCURRENT_TURNS = 8
"""Ceiling on turns handled at once.

aiogram runs every update as its own task and by default imposes no limit at
all. Each turn is cheap — it spends its time waiting on the network, and an
image generation is eighty seconds of idle polling — but "cheap" and "unbounded"
together still add up. This box also runs a VPN other people depend on, so the
process takes a stated share rather than whatever it can get.

Eight is well above what a demo or a handful of operators produce, and far below
what would trouble 2 GB of RAM at ~170 MB resident.
"""


async def run(agent: Agent, bindings: BindingTable, settings: TelegramSettings) -> None:
    """Long-poll for updates. Deployment swaps this for a webhook."""
    bot = Bot(token=settings.bot_token.get_secret_value())
    dispatcher = build_dispatcher(
        TelegramGateway(agent=agent, bindings=bindings, show_steps=settings.show_steps)
    )
    log.info(
        "telegram.starting",
        chats=len(bindings),
        tenants=sorted(bindings.tenants),
        concurrent_turns=CONCURRENT_TURNS,
    )
    try:
        await dispatcher.start_polling(bot, tasks_concurrency_limit=CONCURRENT_TURNS)
    finally:
        await bot.session.close()
