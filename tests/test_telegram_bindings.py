"""The authorization boundary of the messaging surface.

These are the tests that matter most in the project. Everything else decides how
well CONDUIT answers; these decide whether it should have answered at all.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from conduit.interfaces.telegram.bindings import (
    Binding,
    BindingError,
    BindingTable,
    DenialReason,
    load_bindings,
)

KNOWN_CHAT = 111111111
KNOWN_USER = 222222222


@pytest.fixture
def table() -> BindingTable:
    return BindingTable(
        [
            Binding(
                chat_id=KNOWN_CHAT,
                tenant_id="tenant-conduit-demo",
                label="private",
                allowed_user_ids=frozenset({KNOWN_USER}),
            ),
            Binding(
                chat_id=-500,
                tenant_id="tenant-otro",
                label="a permitted group",
                allow_group_chat=True,
            ),
        ]
    )


def write(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "bindings.toml"
    path.write_text(body, encoding="utf-8")
    return path


class TestResolution:
    def test_a_bound_chat_and_sender_is_allowed(self, table: BindingTable) -> None:
        resolution = table.resolve(chat_id=KNOWN_CHAT, user_id=KNOWN_USER, is_private=True)

        assert resolution.allowed
        assert resolution.tenant_id == "tenant-conduit-demo"

    def test_an_unknown_chat_is_denied(self, table: BindingTable) -> None:
        resolution = table.resolve(chat_id=999, user_id=KNOWN_USER, is_private=True)

        assert not resolution.allowed
        assert resolution.reason is DenialReason.UNKNOWN_CHAT

    def test_a_stranger_in_a_bound_chat_is_denied(self, table: BindingTable) -> None:
        """Knowing the chat is not the same as being allowed to speak in it."""
        resolution = table.resolve(chat_id=KNOWN_CHAT, user_id=777, is_private=True)

        assert not resolution.allowed
        assert resolution.reason is DenialReason.SENDER_NOT_ALLOWED

    def test_a_bound_chat_used_as_a_group_is_denied(self, table: BindingTable) -> None:
        """The binding was written for a private conversation."""
        resolution = table.resolve(chat_id=KNOWN_CHAT, user_id=KNOWN_USER, is_private=False)

        assert not resolution.allowed
        assert resolution.reason is DenialReason.GROUP_NOT_ALLOWED

    def test_a_group_that_opted_in_is_allowed(self, table: BindingTable) -> None:
        resolution = table.resolve(chat_id=-500, user_id=777, is_private=False)

        assert resolution.allowed
        assert resolution.tenant_id == "tenant-otro"

    def test_a_denied_resolution_yields_no_tenant(self, table: BindingTable) -> None:
        """There must be no way to read a tenant off a refusal."""
        resolution = table.resolve(chat_id=999, user_id=KNOWN_USER, is_private=True)

        with pytest.raises(BindingError):
            _ = resolution.tenant_id


class TestImmutability:
    def test_the_table_exposes_no_mutation(self, table: BindingTable) -> None:
        """No command, no onboarding flow, no setter. Deployment only."""
        forbidden = {"add", "register", "bind", "set", "update", "remove", "delete"}
        surface = {name for name in dir(table) if not name.startswith("_")}

        assert not (surface & forbidden)

    def test_a_binding_cannot_be_edited_in_place(self, table: BindingTable) -> None:
        binding = table.resolve(chat_id=KNOWN_CHAT, user_id=KNOWN_USER, is_private=True).binding
        assert binding is not None

        with pytest.raises(AttributeError):
            binding.tenant_id = "tenant-not-ours"  # type: ignore[misc]

    def test_the_table_cannot_gain_attributes(self, table: BindingTable) -> None:
        with pytest.raises(AttributeError):
            table.extra = "x"  # type: ignore[attr-defined]


class TestLoading:
    def test_a_valid_file_loads(self, tmp_path: Path) -> None:
        path = write(
            tmp_path,
            """
            [[binding]]
            chat_id = 111
            tenant_id = "tenant-conduit-demo"
            label = "private"
            allowed_user_ids = [222]
            """,
        )

        loaded = load_bindings(path)

        assert len(loaded) == 1
        assert loaded.tenants == {"tenant-conduit-demo"}

    def test_the_shipped_example_parses(self) -> None:
        example = (
            Path(__file__).resolve().parent.parent / "config" / "telegram_bindings.example.toml"
        )

        assert load_bindings(example).tenants == {"tenant-conduit-demo"}

    def test_a_missing_file_is_fatal(self, tmp_path: Path) -> None:
        with pytest.raises(BindingError, match="not found"):
            load_bindings(tmp_path / "absent.toml")

    def test_an_empty_file_refuses_to_start(self, tmp_path: Path) -> None:
        """Starting with zero bindings denies everything, but it is a mistake."""
        with pytest.raises(BindingError):
            load_bindings(write(tmp_path, "# nothing here\n"))

    def test_a_duplicate_chat_is_fatal(self, tmp_path: Path) -> None:
        """Two tenants claiming one chat is not something to resolve by ordering."""
        path = write(
            tmp_path,
            """
            [[binding]]
            chat_id = 111
            tenant_id = "tenant-a"

            [[binding]]
            chat_id = 111
            tenant_id = "tenant-b"
            """,
        )

        with pytest.raises(BindingError, match="bound twice"):
            load_bindings(path)

    def test_a_binding_without_a_tenant_is_fatal(self, tmp_path: Path) -> None:
        path = write(tmp_path, "[[binding]]\nchat_id = 111\n")

        with pytest.raises(BindingError, match="tenant_id"):
            load_bindings(path)

    def test_broken_toml_is_fatal(self, tmp_path: Path) -> None:
        with pytest.raises(BindingError, match="not valid TOML"):
            load_bindings(write(tmp_path, "[[binding]\nchat_id = "))
