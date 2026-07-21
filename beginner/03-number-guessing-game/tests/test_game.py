"""Tests for the pure game logic (deterministic via a seeded random source)."""

from __future__ import annotations

import random

import pytest

from number_guessing_game.config import DIFFICULTIES
from number_guessing_game.game import (
    Game,
    GuessOutcome,
    difficulty_by_name,
    new_game,
)


def test_new_game_is_deterministic_with_a_seed() -> None:
    first = new_game(DIFFICULTIES["hard"], random.Random(42))
    second = new_game(DIFFICULTIES["hard"], random.Random(42))
    assert first.secret == second.secret


def test_guess_outcomes() -> None:
    game = Game(1, 100, 10, secret=50)
    assert game.guess(25) is GuessOutcome.TOO_LOW
    assert game.guess(75) is GuessOutcome.TOO_HIGH
    assert game.guess(50) is GuessOutcome.CORRECT
    assert game.has_won
    assert game.is_over


def test_guess_out_of_range_raises() -> None:
    game = Game(1, 10, 5, secret=5)
    with pytest.raises(ValueError, match="between 1 and 10"):
        game.guess(11)


def test_running_out_of_attempts_ends_the_game() -> None:
    game = Game(1, 100, 3, secret=50)
    for value in (10, 20, 30):
        game.guess(value)
    assert game.is_over
    assert not game.has_won
    assert game.attempts_remaining == 0


def test_guessing_after_game_over_raises() -> None:
    game = Game(1, 10, 1, secret=5)
    game.guess(1)
    with pytest.raises(RuntimeError):
        game.guess(2)


def test_secret_outside_range_is_rejected() -> None:
    with pytest.raises(ValueError, match="within the range"):
        Game(1, 10, 5, secret=99)


def test_difficulty_lookup() -> None:
    assert difficulty_by_name("easy").low == 1
    with pytest.raises(ValueError, match="unknown difficulty"):
        difficulty_by_name("impossible")
