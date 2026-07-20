"""Tests for applying and undoing moves, including partial failure."""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from file_organizer.classify import default_rules
from file_organizer.executor import apply_plan, undo_moves
from file_organizer.models import Move
from file_organizer.planner import build_plan


def _touch(path: Path, name: str, content: str = "x") -> Path:
    file = path / name
    file.write_text(content, encoding="utf-8")
    return file


def test_apply_moves_files(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.jpg")
    _touch(source, "b.txt")
    destination = tmp_path / "dst"

    plan = build_plan(source, destination, default_rules())
    result = apply_plan(plan.moves)

    assert result.ok
    assert (destination / "images" / "a.jpg").is_file()
    assert (destination / "documents" / "b.txt").is_file()
    assert not (source / "a.jpg").exists()


def test_apply_never_overwrites(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    file = _touch(source, "a.jpg", "new")
    destination = tmp_path / "dst" / "images" / "a.jpg"
    destination.parent.mkdir(parents=True)
    destination.write_text("old", encoding="utf-8")

    move = Move(source=file, destination=destination, category="images")
    result = apply_plan((move,))

    assert not result.ok
    assert destination.read_text(encoding="utf-8") == "old"  # untouched


def test_partial_failure_is_reported(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.jpg")
    _touch(source, "b.txt")
    plan = build_plan(source, tmp_path / "dst", default_rules())

    real_move = shutil.move
    calls = {"n": 0}

    def flaky(src: str, dst: str) -> object:
        calls["n"] += 1
        if calls["n"] == 2:
            raise OSError("simulated failure")
        return real_move(src, dst)

    monkeypatch.setattr(shutil, "move", flaky)
    result = apply_plan(plan.moves)

    assert not result.ok
    assert len(result.completed) == 1
    assert result.failure is not None


def test_undo_restores_moves(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.jpg")
    plan = build_plan(source, tmp_path / "dst", default_rules())
    result = apply_plan(plan.moves)

    undo = undo_moves(list(result.completed))

    assert len(undo.restored) == 1
    assert (source / "a.jpg").is_file()


def test_undo_refuses_when_original_occupied(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    original = _touch(source, "a.jpg")
    plan = build_plan(source, tmp_path / "dst", default_rules())
    result = apply_plan(plan.moves)
    # Recreate a file at the original path so undo would have to overwrite.
    original.write_text("blocker", encoding="utf-8")

    undo = undo_moves(list(result.completed))

    assert not undo.restored
    assert undo.skipped[0][1] == "original path is occupied"


def test_undo_skips_missing_moved_file(tmp_path: Path) -> None:
    move = Move(
        source=tmp_path / "src" / "a.jpg",
        destination=tmp_path / "dst" / "images" / "a.jpg",
        category="images",
    )
    undo = undo_moves([move])
    assert not undo.restored
    assert undo.skipped[0][1] == "moved file is missing"
