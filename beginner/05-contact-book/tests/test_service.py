"""Tests for CRUD and search logic."""

from __future__ import annotations

import pytest

from contact_book.errors import ContactNotFoundError, ValidationError
from contact_book.models import Contact
from contact_book.service import (
    create_contact,
    delete_contact,
    find_contacts,
    get_contact,
    update_contact,
)


def _fixed_id() -> str:
    return "id000001"


def test_create_contact_trims_and_validates() -> None:
    contact = create_contact(
        name="  Ada Lovelace  ",
        email="ada@example.com",
        phone="+1 (555) 123-4567",
        id_factory=_fixed_id,
    )
    assert contact.name == "Ada Lovelace"
    assert contact.email == "ada@example.com"
    assert contact.id == "id000001"


def test_create_rejects_empty_name() -> None:
    with pytest.raises(ValidationError, match="name"):
        create_contact(name="   ")


def test_create_rejects_bad_email_and_phone() -> None:
    with pytest.raises(ValidationError, match="email"):
        create_contact(name="A", email="not-an-email")
    with pytest.raises(ValidationError, match="phone"):
        create_contact(name="A", phone="12")


def _sample() -> list[Contact]:
    return [
        Contact("1", "Ada Lovelace", "ada@example.com", "5551234567"),
        Contact("2", "Alan Turing", "alan@example.com", None),
        Contact("3", "Grace Hopper", None, "5559876543"),
    ]


def test_find_by_name_case_insensitive() -> None:
    assert {c.id for c in find_contacts(_sample(), "ALAN")} == {"2"}


def test_find_by_email_and_phone() -> None:
    assert {c.id for c in find_contacts(_sample(), "example.com")} == {"1", "2"}
    assert {c.id for c in find_contacts(_sample(), "9876")} == {"3"}


def test_empty_query_returns_all() -> None:
    assert len(find_contacts(_sample(), "  ")) == 3


def test_get_contact_found_and_missing() -> None:
    assert get_contact(_sample(), "2").name == "Alan Turing"
    with pytest.raises(ContactNotFoundError):
        get_contact(_sample(), "nope")


def test_update_changes_only_given_fields() -> None:
    updated_list, contact = update_contact(_sample(), "1", phone="5550000000")
    assert contact.phone == "5550000000"
    assert contact.email == "ada@example.com"  # unchanged
    assert any(c.phone == "5550000000" for c in updated_list)


def test_update_missing_and_invalid() -> None:
    with pytest.raises(ContactNotFoundError):
        update_contact(_sample(), "nope", name="X")
    with pytest.raises(ValidationError):
        update_contact(_sample(), "1", email="bad")


def test_delete_existing_and_missing() -> None:
    assert {c.id for c in delete_contact(_sample(), "2")} == {"1", "3"}
    with pytest.raises(ContactNotFoundError):
        delete_contact(_sample(), "nope")
