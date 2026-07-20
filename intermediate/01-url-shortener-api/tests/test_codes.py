"""Tests for short-code generation."""

from __future__ import annotations

from url_shortener.application.codes import ALPHABET, generate_code


def test_generated_code_has_requested_length() -> None:
    assert len(generate_code(7)) == 7


def test_generated_code_uses_only_alphabet() -> None:
    code = generate_code(20)
    assert all(character in ALPHABET for character in code)
