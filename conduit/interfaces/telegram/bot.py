"""Telegram surface: resolve the conversation, then hand off to the agent.

Replies are sent as plain text with no parse mode. The demo tenant deliberately
contains a surname with an apostrophe and others with accents, and Markdown
escaping is a reliable source of either mangled names or failed sends. Plain text
has neither failure mode.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass

import structlog
from aiogram import Bot, Dispatcher
from aiogram.types import Message

from conduit.core.agent import Agent
from conduit.core.tools import ToolContext
from conduit.interfaces.telegram.bindings import BindingTable, Resolution
from conduit.interfaces.telegram.config import TelegramSettings

__all__ = ["REFUSAL", "TelegramGateway", "build_dispatcher"]

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

        ctx = ToolContext(
            tenant_id=binding.tenant_id,
            session_id=f"telegram:{chat.id}",
            actor_id=f"telegram:{sender.id}",
            request_id=uuid.uuid4().hex,
            idempotency_key=f"tg-{chat.id}-{message.message_id}",
        )

        try:
            reply = await self.agent.run(text, ctx)
        # The interface is the last line: a crash here is a silent bot.
        except Exception:
            log.exception(
                "telegram.turn_failed",
                tenant_id=binding.tenant_id,
                session_id=ctx.session_id,
                request_id=ctx.request_id,
            )
            return PROBLEM

        log.info(
            "telegram.turn",
            tenant_id=binding.tenant_id,
            session_id=ctx.session_id,
            request_id=ctx.request_id,
            stop_reason=reply.stop_reason.value,
            calls=len(reply.calls),
        )
        return reply.text or PROBLEM

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


async def run(agent: Agent, bindings: BindingTable, settings: TelegramSettings) -> None:
    """Long-poll for updates. Deployment swaps this for a webhook."""
    bot = Bot(token=settings.bot_token.get_secret_value())
    dispatcher = build_dispatcher(TelegramGateway(agent=agent, bindings=bindings))
    log.info("telegram.starting", chats=len(bindings), tenants=sorted(bindings.tenants))
    try:
        await dispatcher.start_polling(bot)
    finally:
        await bot.session.close()
