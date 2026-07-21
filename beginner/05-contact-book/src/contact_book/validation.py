"""Basic field validation.

These checks catch common mistakes; they are intentionally simple and are **not**
a universal validator for names, emails, or phone numbers.
"""

from __future__ import annotations

import re

from .errors import ValidationError

NAME_MAX_LENGTH = 100
_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
_PHONE_ALLOWED = re.compile(r"^[0-9()+\-\s]+$")
_MIN_PHONE_DIGITS = 7


def validate_name(name: str) -> str:
    cleaned = name.strip()
    if not cleaned:
        raise ValidationError("name must not be empty")
    if len(cleaned) > NAME_MAX_LENGTH:
        raise ValidationError(f"name must be at most {NAME_MAX_LENGTH} characters")
    return cleaned


def validate_email(email: str | None) -> str | None:
    if email is None:
        return None
    cleaned = email.strip()
    if not cleaned:
        return None
    if not _EMAIL.match(cleaned):
        raise ValidationError(f"email {email!r} does not look like an email address")
    return cleaned


def validate_phone(phone: str | None) -> str | None:
    if phone is None:
        return None
    cleaned = phone.strip()
    if not cleaned:
        return None
    digits = sum(character.isdigit() for character in cleaned)
    if not _PHONE_ALLOWED.match(cleaned) or digits < _MIN_PHONE_DIGITS:
        raise ValidationError(
            f"phone {phone!r} must have at least {_MIN_PHONE_DIGITS} digits and "
            "use only digits, spaces, +, -, (, )"
        )
    return cleaned
