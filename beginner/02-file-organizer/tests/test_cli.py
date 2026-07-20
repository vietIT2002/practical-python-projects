"""End-to-end tests for the command-line interface."""

from __future__ import annotations

from pathlib import Path

import pytest

from file_organizer.cli import main


def _touch(path: Path, name: str) -> Path:
    file = path / name
    file.write_text("x", encoding="utf-8")
    return file


def test_organize_dry_run_moves_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.jpg")
    destination = tmp_path / "dst"

    exit_code = main(["organize", str(source), str(destination)])

    assert exit_code == 0
    assert "Dry run" in capsys.readouterr().out
    assert (source / "a.jpg").exists()
    assert not destination.exists()


def test_organize_apply_moves_and_writes_manifest(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.jpg")
    destination = tmp_path / "dst"

    exit_code = main(["organize", str(source), str(destination), "--apply"])

    assert exit_code == 0
    assert (destination / "images" / "a.jpg").is_file()
    assert (destination / "file-organizer-manifest.json").is_file()


def test_undo_round_trip(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.jpg")
    destination = tmp_path / "dst"
    main(["organize", str(source), str(destination), "--apply"])
    manifest = destination / "file-organizer-manifest.json"
    capsys.readouterr()

    exit_code = main(["undo", str(manifest), "--apply"])

    assert exit_code == 0
    assert "Restored 1" in capsys.readouterr().out
    assert (source / "a.jpg").is_file()


def test_undo_dry_run_restores_nothing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "src"
    source.mkdir()
    _touch(source, "a.jpg")
    destination = tmp_path / "dst"
    main(["organize", str(source), str(destination), "--apply"])
    manifest = destination / "file-organizer-manifest.json"
    capsys.readouterr()

    exit_code = main(["undo", str(manifest)])

    assert exit_code == 0
    assert "Dry run" in capsys.readouterr().out
    assert (destination / "images" / "a.jpg").is_file()  # still moved, not restored


def test_organize_bad_source_returns_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(["organize", str(tmp_path / "missing"), str(tmp_path / "dst")])
    assert exit_code == 1
    assert "error" in capsys.readouterr().err
