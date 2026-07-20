"""Tests for the internal Markdown link checker."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.check_internal_links import find_broken_links, main


def test_broken_file_link_is_reported(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("[x](missing.md)\n", encoding="utf-8")
    problems = find_broken_links(tmp_path)
    assert any("broken link" in p for p in problems)


def test_valid_link_and_external_and_anchor(tmp_path: Path) -> None:
    (tmp_path / "target.md").write_text("# Title\n", encoding="utf-8")
    (tmp_path / "a.md").write_text(
        "[ok](target.md) [ext](https://example.com) [mail](mailto:a@b.c) "
        "[anchor](target.md#title)\n",
        encoding="utf-8",
    )
    assert find_broken_links(tmp_path) == []


def test_self_anchor_and_missing_anchor(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text(
        "# Intro\n[here](#intro) and [nope](#missing)\n", encoding="utf-8"
    )
    problems = find_broken_links(tmp_path)
    assert any("missing anchor '#missing'" in p for p in problems)
    assert all("#intro" not in p for p in problems)


def test_missing_cross_file_anchor(tmp_path: Path) -> None:
    (tmp_path / "target.md").write_text("# Title\n", encoding="utf-8")
    (tmp_path / "a.md").write_text("[x](target.md#nope)\n", encoding="utf-8")
    assert any("missing anchor" in p for p in find_broken_links(tmp_path))


def test_excluded_directories_are_skipped(tmp_path: Path) -> None:
    hidden = tmp_path / ".ai"
    hidden.mkdir()
    (hidden / "note.md").write_text("[x](missing.md)\n", encoding="utf-8")
    assert find_broken_links(tmp_path) == []


def test_main_clean_and_broken(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (tmp_path / "a.md").write_text("[ok](https://example.com)\n", encoding="utf-8")
    assert main(["--root", str(tmp_path)]) == 0
    capsys.readouterr()
    (tmp_path / "b.md").write_text("[bad](nope.md)\n", encoding="utf-8")
    assert main(["--root", str(tmp_path)]) == 1
    assert "broken internal link" in capsys.readouterr().out
