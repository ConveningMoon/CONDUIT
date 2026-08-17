"""Which conversation may act for which tenant.

This module is the authorization boundary of the messaging surface. It mirrors
the rule the CRM enforces on its own side: the credential decides the tenant, and
the client cannot ask for a different one. Here the binding file plays the part
of the credential.

Three properties hold, and each is a test:

1. **Nothing in a message can change a binding.** There is no registration
   command, no onboarding flow, no setter — not even a private one. The file is
   read once at startup and frozen. Changing it means a deployment and a diff
   somebody reviewed.
2. **An unknown conversation is denied.** Absence is never treated as permission.
3. **A group is denied unless the binding says otherwise.** An authorized person
   in a room full of strangers is not authorization to read a tenant's business
   out loud.
"""

from __future__ import annotations

import tomllib
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

__all__ = [
    "Binding",
    "BindingError",
    "BindingTable",
    "DenialReason",
    "Resolution",
    "load_bindings",
]


class BindingError(RuntimeError):
    """The binding file is unusable. Always fatal: never start without it."""


class DenialReason(StrEnum):
    UNKNOWN_CHAT = "unknown_chat"
    SENDER_NOT_ALLOWED = "sender_not_allowed"
    GROUP_NOT_ALLOWED = "group_not_allowed"


@dataclass(frozen=True, slots=True)
class Binding:
    """One conversation, bound to one tenant."""

    chat_id: int
    tenant_id: str
    label: str
    allowed_user_ids: frozenset[int] = field(default_factory=frozenset)
    """Senders permitted in this chat. Empty means any sender the chat allows,
    which is only sensible for a private chat with a single human in it."""

    allow_group_chat: bool = False

    def permits(self, *, user_id: int, is_private: bool) -> DenialReason | None:
        if not is_private and not self.allow_group_chat:
            return DenialReason.GROUP_NOT_ALLOWED
        if self.allowed_user_ids and user_id not in self.allowed_user_ids:
            return DenialReason.SENDER_NOT_ALLOWED
        return None


@dataclass(frozen=True, slots=True)
class Resolution:
    """Outcome of resolving one incoming message."""

    binding: Binding | None
    reason: DenialReason | None

    @property
    def allowed(self) -> bool:
        return self.binding is not None and self.reason is None

    @property
    def tenant_id(self) -> str:
        if self.binding is None:
            raise BindingError("no tenant on a denied resolution")
        return self.binding.tenant_id

    @classmethod
    def deny(cls, reason: DenialReason) -> Resolution:
        return cls(binding=None, reason=reason)

    @classmethod
    def allow(cls, binding: Binding) -> Resolution:
        return cls(binding=binding, reason=None)


class BindingTable:
    """Immutable lookup from chat to tenant.

    Deliberately offers no way to add, remove or modify a binding. If a future
    version stores these in Postgres, the same applies: writes come from an
    administrative path, never from the agent and never from a conversation.
    """

    __slots__ = ("_by_chat",)

    def __init__(self, bindings: list[Binding]) -> None:
        by_chat: dict[int, Binding] = {}
        for binding in bindings:
            if binding.chat_id in by_chat:
                raise BindingError(
                    f"chat_id {binding.chat_id} is bound twice; "
                    "an ambiguous binding is not something to guess about"
                )
            by_chat[binding.chat_id] = binding
        if not by_chat:
            raise BindingError("no bindings configured; refusing to start deaf")
        self._by_chat = by_chat

    def __len__(self) -> int:
        return len(self._by_chat)

    @property
    def tenants(self) -> set[str]:
        return {binding.tenant_id for binding in self._by_chat.values()}

    def resolve(self, *, chat_id: int, user_id: int, is_private: bool) -> Resolution:
        """Decide whether this message may act, and for whom."""
        binding = self._by_chat.get(chat_id)
        if binding is None:
            return Resolution.deny(DenialReason.UNKNOWN_CHAT)
        refusal = binding.permits(user_id=user_id, is_private=is_private)
        if refusal is not None:
            return Resolution.deny(refusal)
        return Resolution.allow(binding)


def load_bindings(path: Path) -> BindingTable:
    """Read the binding file. Any doubt is fatal rather than permissive."""
    if not path.is_file():
        raise BindingError(f"binding file not found: {path}")

    try:
        document = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise BindingError(f"binding file is not valid TOML: {exc}") from exc

    entries = document.get("binding")
    if not isinstance(entries, list):
        raise BindingError("binding file must contain at least one [[binding]] table")

    bindings: list[Binding] = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise BindingError(f"binding #{index} is not a table")
        try:
            bindings.append(
                Binding(
                    chat_id=int(entry["chat_id"]),
                    tenant_id=str(entry["tenant_id"]),
                    label=str(entry.get("label", "")),
                    allowed_user_ids=frozenset(
                        int(uid) for uid in entry.get("allowed_user_ids", [])
                    ),
                    allow_group_chat=bool(entry.get("allow_group_chat", False)),
                )
            )
        except KeyError as exc:
            raise BindingError(f"binding #{index} is missing {exc.args[0]!r}") from exc
        except (TypeError, ValueError) as exc:
            raise BindingError(f"binding #{index} has an unreadable field: {exc}") from exc

    return BindingTable(bindings)
