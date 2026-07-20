"""Apply a plan and undo a manifest, reporting partial failure honestly."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, field

from .models import Move


@dataclass(frozen=True)
class ApplyResult:
    """Outcome of applying a plan."""

    completed: tuple[Move, ...]
    failure: Move | None = None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.failure is None


@dataclass
class UndoResult:
    """Outcome of undoing a manifest."""

    restored: list[Move] = field(default_factory=list)
    skipped: list[tuple[Move, str]] = field(default_factory=list)


def apply_plan(plan_moves: tuple[Move, ...]) -> ApplyResult:
    """Move each planned file into place.

    Stops at the first failure and reports which moves completed, so a partial
    run is never silent. Never overwrites an existing destination.
    """
    completed: list[Move] = []
    for move in plan_moves:
        try:
            move.destination.parent.mkdir(parents=True, exist_ok=True)
            if move.destination.exists():
                return ApplyResult(
                    tuple(completed),
                    move,
                    f"destination already exists: {move.destination}",
                )
            shutil.move(os.fspath(move.source), os.fspath(move.destination))
        except OSError as exc:
            return ApplyResult(tuple(completed), move, str(exc))
        completed.append(move)
    return ApplyResult(tuple(completed))


def undo_moves(moves: list[Move]) -> UndoResult:
    """Reverse each move (destination back to source).

    Refuses any reversal that would be unsafe or ambiguous: if the moved file is
    missing, or the original path is now occupied, that entry is skipped rather
    than risking data loss.
    """
    result = UndoResult()
    for move in moves:
        if not move.destination.exists():
            result.skipped.append((move, "moved file is missing"))
            continue
        if move.source.exists():
            result.skipped.append((move, "original path is occupied"))
            continue
        try:
            move.source.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(os.fspath(move.destination), os.fspath(move.source))
        except OSError as exc:
            result.skipped.append((move, str(exc)))
            continue
        result.restored.append(move)
    return result
