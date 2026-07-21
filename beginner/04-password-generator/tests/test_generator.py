"""Tests for password generation.

Generation is random, so these assert guaranteed properties (length, group
membership, character set) rather than exact values.
"""

from __future__ import annotations

import string

import pytest

from password_generator.errors import PolicyError
from password_generator.generator import (
    _secure_shuffle,
    generate_password,
    generate_passwords,
)
from password_generator.policy import DIGITS, SYMBOLS, Policy


def test_generated_length_matches_policy() -> None:
    assert len(generate_password(Policy(length=20))) == 20


def test_every_selected_group_is_present() -> None:
    password = generate_password(Policy(length=8, use_symbols=True))
    assert any(c in string.ascii_lowercase for c in password)
    assert any(c in string.ascii_uppercase for c in password)
    assert any(c in DIGITS for c in password)
    assert any(c in SYMBOLS for c in password)


def test_excluded_groups_never_appear() -> None:
    policy = Policy(length=12, use_uppercase=False, use_digits=False)
    password = generate_password(policy)
    assert all(c in string.ascii_lowercase for c in password)


def test_generate_multiple() -> None:
    passwords = generate_passwords(Policy(length=10), 5)
    assert len(passwords) == 5
    assert all(len(p) == 10 for p in passwords)


def test_generate_count_must_be_positive() -> None:
    with pytest.raises(PolicyError, match="count"):
        generate_passwords(Policy(), 0)


def test_secure_shuffle_preserves_multiset() -> None:
    items = list("abcdef")
    _secure_shuffle(items)
    assert sorted(items) == list("abcdef")
