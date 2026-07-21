"""Tests for the basic field validators."""

from __future__ import annotations

import pytest

from contact_book.errors import ValidationError
from contact_book.validation import validate_email, validate_name, validate_phone


def test_blank_optional_fields_become_none() -> None:
    assert validate_email("  ") is None
    assert validate_phone(None) is None
    assert validate_email(None) is None


def test_valid_optional_fields() -> None:
    assert validate_email("a@b.co") == "a@b.co"
    assert validate_phone("+1 555 123 4567") == "+1 555 123 4567"


def test_name_too_long() -> None:
    with pytest.raises(ValidationError, match="at most"):
        validate_name("x" * 101)


def test_phone_with_letters_rejected() -> None:
    with pytest.raises(ValidationError, match="phone"):
        validate_phone("call-me")
