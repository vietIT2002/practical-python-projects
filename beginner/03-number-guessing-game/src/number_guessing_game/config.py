"""Difficulty definitions for the guessing game."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Difficulty:
    """A named difficulty: an inclusive range and a maximum number of attempts."""

    name: str
    low: int
    high: int
    max_attempts: int


DIFFICULTIES: dict[str, Difficulty] = {
    "easy": Difficulty("easy", 1, 10, 5),
    "medium": Difficulty("medium", 1, 50, 8),
    "hard": Difficulty("hard", 1, 100, 10),
}

DEFAULT_DIFFICULTY = "medium"
