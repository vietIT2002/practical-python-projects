"""Build a move plan without changing the filesystem.

Planning is deliberately pure: it reads the source directory and computes where
each file would go, but it never creates, moves, or deletes anything.
"""

from __future__ import annotations

from pathlib import Path

from .classify import category_for
from .errors import PlanError
from .models import Move, Plan, Skip


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _resolve_conflict(destination: Path, claimed: set[Path]) -> Path:
    """Return a destination path that neither exists nor is already claimed.

    Conflicts are resolved deterministically by appending " (1)", " (2)", …
    before the extension, so a run never overwrites an existing file.
    """
    if not destination.exists() and destination not in claimed:
        return destination
    stem, suffix = destination.stem, destination.suffix
    counter = 1
    while True:
        candidate = destination.with_name(f"{stem} ({counter}){suffix}")
        if not candidate.exists() and candidate not in claimed:
            return candidate
        counter += 1


def build_plan(source: Path, destination: Path, rules: dict[str, str]) -> Plan:
    """Plan how to organise files from ``source`` into ``destination``.

    Only the direct contents of ``source`` are considered (no recursion).
    Directories and symlinks are skipped, and every destination is kept inside
    the destination root.
    """
    source = source.expanduser().resolve()
    destination = destination.expanduser().resolve()

    if not source.is_dir():
        raise PlanError(f"source is not a directory: {source}")
    if source == destination:
        raise PlanError("source and destination must be different directories")

    moves: list[Move] = []
    skipped: list[Skip] = []
    claimed: set[Path] = set()

    for entry in sorted(source.iterdir()):
        if entry.is_symlink():
            skipped.append(Skip(entry, "symlink"))
            continue
        if entry.is_dir():
            skipped.append(Skip(entry, "directory"))
            continue

        category = category_for(entry.name, rules)
        proposed = destination / category / entry.name
        if not _is_within(proposed, destination):
            skipped.append(Skip(entry, f"unsafe category {category!r}"))
            continue

        target = _resolve_conflict(proposed, claimed)
        claimed.add(target)
        moves.append(Move(source=entry, destination=target, category=category))

    return Plan(moves=tuple(moves), skipped=tuple(skipped))
