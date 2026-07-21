"""CRUD and search logic for contacts (pure functions)."""

from __future__ import annotations

from collections.abc import Callable, Iterable
from uuid import uuid4

from .errors import ContactNotFoundError
from .models import Contact
from .validation import validate_email, validate_name, validate_phone

IdFactory = Callable[[], str]


def _default_id() -> str:
    return uuid4().hex[:8]


def create_contact(
    *,
    name: str,
    email: str | None = None,
    phone: str | None = None,
    id_factory: IdFactory = _default_id,
) -> Contact:
    """Validate input and build a :class:`Contact`."""
    return Contact(
        id=id_factory(),
        name=validate_name(name),
        email=validate_email(email),
        phone=validate_phone(phone),
    )


def find_contacts(contacts: Iterable[Contact], query: str) -> list[Contact]:
    """Return contacts whose name, email, or phone contains ``query``.

    Matching is case-insensitive; an empty query returns all contacts.
    """
    needle = query.strip().casefold()
    if not needle:
        return list(contacts)
    matches = []
    for contact in contacts:
        haystack = " ".join(
            part for part in (contact.name, contact.email, contact.phone) if part
        ).casefold()
        if needle in haystack:
            matches.append(contact)
    return matches


def get_contact(contacts: Iterable[Contact], contact_id: str) -> Contact:
    for contact in contacts:
        if contact.id == contact_id:
            return contact
    raise ContactNotFoundError(f"no contact found with id {contact_id!r}")


def update_contact(
    contacts: Iterable[Contact],
    contact_id: str,
    *,
    name: str | None = None,
    email: str | None = None,
    phone: str | None = None,
) -> tuple[list[Contact], Contact]:
    """Return the updated list and the updated contact.

    Only the fields that are provided (not ``None``) are changed.
    """
    original = list(contacts)
    existing = get_contact(original, contact_id)
    updated = Contact(
        id=existing.id,
        name=validate_name(name) if name is not None else existing.name,
        email=validate_email(email) if email is not None else existing.email,
        phone=validate_phone(phone) if phone is not None else existing.phone,
    )
    result = [updated if c.id == contact_id else c for c in original]
    return result, updated


def delete_contact(contacts: Iterable[Contact], contact_id: str) -> list[Contact]:
    original = list(contacts)
    remaining = [contact for contact in original if contact.id != contact_id]
    if len(remaining) == len(original):
        raise ContactNotFoundError(f"no contact found with id {contact_id!r}")
    return remaining
