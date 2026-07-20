"""Typed records describing planned and completed moves."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Move:
    """A single planned or completed move of one file into a category folder."""

    source: Path
    destination: Path
    category: str


@dataclass(frozen=True)
class Skip:
    """A file or entry that will not be moved, with a human-readable reason."""

    path: Path
    reason: str


@dataclass(frozen=True)
class Plan:
    """The result of planning: what would move and what would be skipped."""

    moves: tuple[Move, ...]
    skipped: tuple[Skip, ...]
