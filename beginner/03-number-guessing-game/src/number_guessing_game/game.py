"""The pure game state machine.

No input, output, or global random state lives here, so the game is fully
deterministic under test when given a seeded random source.
"""

from __future__ import annotations

import random
from enum import Enum

from .config import DIFFICULTIES, Difficulty


class GuessOutcome(Enum):
    TOO_LOW = "too_low"
    TOO_HIGH = "too_high"
    CORRECT = "correct"


class Game:
    """Tracks the secret number, attempts, and win state for one round."""

    def __init__(self, low: int, high: int, max_attempts: int, secret: int) -> None:
        if not low <= secret <= high:
            raise ValueError("secret must be within the range")
        self.low = low
        self.high = high
        self.max_attempts = max_attempts
        self._secret = secret
        self._attempts = 0
        self._won = False

    def guess(self, value: int) -> GuessOutcome:
        """Register a guess and return whether it is low, high, or correct."""
        if self.is_over:
            raise RuntimeError("the game is already over")
        if not self.low <= value <= self.high:
            raise ValueError(f"guess must be between {self.low} and {self.high}")
        self._attempts += 1
        if value == self._secret:
            self._won = True
            return GuessOutcome.CORRECT
        return GuessOutcome.TOO_LOW if value < self._secret else GuessOutcome.TOO_HIGH

    @property
    def attempts_made(self) -> int:
        return self._attempts

    @property
    def attempts_remaining(self) -> int:
        return self.max_attempts - self._attempts

    @property
    def has_won(self) -> bool:
        return self._won

    @property
    def is_over(self) -> bool:
        return self._won or self._attempts >= self.max_attempts

    @property
    def secret(self) -> int:
        """The secret number (used to reveal it once the game is over)."""
        return self._secret


def new_game(difficulty: Difficulty, rng: random.Random) -> Game:
    """Create a game for a difficulty, drawing the secret from ``rng``.

    Passing a seeded :class:`random.Random` makes the game deterministic.
    """
    secret = rng.randint(difficulty.low, difficulty.high)
    return Game(difficulty.low, difficulty.high, difficulty.max_attempts, secret)


def difficulty_by_name(name: str) -> Difficulty:
    try:
        return DIFFICULTIES[name]
    except KeyError:
        raise ValueError(f"unknown difficulty {name!r}") from None
