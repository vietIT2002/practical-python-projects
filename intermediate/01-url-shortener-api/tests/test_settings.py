"""Tests for configuration validation."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from url_shortener.settings import Settings


def test_defaults_are_safe() -> None:
    settings = Settings()
    assert settings.database_url.startswith("sqlite")
    assert settings.base_url.startswith("http")


def test_code_length_lower_bound_is_validated() -> None:
    with pytest.raises(ValidationError):
        Settings(code_length=2)
