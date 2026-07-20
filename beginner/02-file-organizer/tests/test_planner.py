"""Tests for the pure planning step."""

from __future__ import annotations

from pathlib import Path

import pytest

from file_organizer.classify import default_rules
from file_organizer.errors import PlanError
from file_organizer.planner import build_plan


def _touch(path: Path, name: str) -> Path:
    file = path / name
    file.write_text("x", encoding="utf-8")
    return file


def test_planning_makes_no_filesystem_changes(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.jpg")
    destination = tmp_path / "dst"

    plan = build_plan(source, destination, default_rules())

    assert len(plan.moves) == 1
    assert (source / "a.jpg").exists()  # nothing moved
    assert not destination.exists()  # nothing created


def test_categories_assigned(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "photo.JPG")
    _touch(source, "notes.md")
    _touch(source, "mystery.xyz")

    plan = build_plan(source, tmp_path / "dst", default_rules())

    categories = {move.source.name: move.category for move in plan.moves}
    assert categories == {
        "photo.JPG": "images",
        "notes.md": "documents",
        "mystery.xyz": "other",
    }


def test_directories_are_skipped(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    (source / "subdir").mkdir()
    _touch(source, "a.txt")

    plan = build_plan(source, tmp_path / "dst", default_rules())

    assert [m.source.name for m in plan.moves] == ["a.txt"]
    assert any(s.reason == "directory" for s in plan.skipped)


def test_symlinks_are_skipped(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    target = _touch(source, "real.txt")
    link = source / "link.txt"
    try:
        link.symlink_to(target)
    except OSError:
        pytest.skip("symlinks not permitted in this environment")

    plan = build_plan(source, tmp_path / "dst", default_rules())

    assert any(s.reason == "symlink" for s in plan.skipped)
    assert all(m.source.name != "link.txt" for m in plan.moves)


def test_name_conflict_gets_suffix(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.jpg")
    # A file already occupies the destination.
    existing = tmp_path / "dst" / "images" / "a.jpg"
    existing.parent.mkdir(parents=True)
    existing.write_text("existing", encoding="utf-8")

    plan = build_plan(source, tmp_path / "dst", default_rules())

    assert plan.moves[0].destination.name == "a (1).jpg"


def test_source_must_be_directory(tmp_path: Path) -> None:
    with pytest.raises(PlanError, match="not a directory"):
        build_plan(tmp_path / "missing", tmp_path / "dst", default_rules())


def test_source_and_destination_must_differ(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    with pytest.raises(PlanError, match="must be different"):
        build_plan(source, source, default_rules())


def test_unsafe_category_is_skipped(tmp_path: Path) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.evil")
    # A hand-built rule with a traversing category (bypassing config validation).
    rules = {".evil": "../escape"}

    plan = build_plan(source, tmp_path / "dst", rules)

    assert not plan.moves
    assert any("unsafe category" in s.reason for s in plan.skipped)
