"""Tests for password policy validation."""

from __future__ import annotations

import pytest

from password_generator.errors import PolicyError
from password_generator.policy import Policy


def test_default_policy_selects_three_groups() -> None:
    assert len(Policy().validate()) == 3


def test_symbols_add_a_group() -> None:
    assert len(Policy(use_symbols=True).validate()) == 4


def test_no_groups_is_rejected() -> None:
    policy = Policy(
        use_lowercase=False,
        use_uppercase=False,
        use_digits=False,
        use_symbols=False,
    )
    with pytest.raises(PolicyError, match="at least one"):
        policy.validate()


def test_length_below_minimum_is_rejected() -> None:
    with pytest.raises(PolicyError, match="between"):
        Policy(length=2).validate()


def test_length_above_maximum_is_rejected() -> None:
    with pytest.raises(PolicyError, match="between"):
        Policy(length=999).validate()
