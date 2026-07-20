"""Tests for the project metadata validator."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.validate_project_metadata import main, scan_projects, validate_project

VALID_METADATA = """\
schema_version = 1
id = "beginner-01"
slug = "expense-tracker"
title = "Expense Tracker CLI"
level = "beginner"
status = "complete"
featured = true
summary = "Track expenses from the command line."
python = ">=3.12"
interfaces = ["cli"]
concepts = ["decimal", "csv"]
prerequisites = ["functions"]
tags = ["cli", "files"]
"""


def _write_project(
    root: Path,
    level: str,
    folder: str,
    metadata: str,
    *,
    with_readme: bool = True,
    with_tests: bool = True,
) -> Path:
    project = root / level / folder
    project.mkdir(parents=True)
    (project / "project.toml").write_text(metadata, encoding="utf-8")
    if with_readme:
        (project / "README.md").write_text("# Project\n", encoding="utf-8")
    if with_tests:
        tests = project / "tests"
        tests.mkdir()
        (tests / "test_smoke.py").write_text(
            "def test_ok():\n    assert True\n", encoding="utf-8"
        )
    return project


def test_valid_complete_project_passes(tmp_path: Path) -> None:
    _write_project(tmp_path, "beginner", "01-expense-tracker", VALID_METADATA)
    assert scan_projects(tmp_path) == []


def test_empty_repository_passes(tmp_path: Path) -> None:
    assert scan_projects(tmp_path) == []


def test_missing_metadata_file_is_reported(tmp_path: Path) -> None:
    project = tmp_path / "beginner" / "01-expense-tracker"
    project.mkdir(parents=True)
    problems, data = validate_project(project, tmp_path)
    assert data == {}
    assert any("missing metadata file" in p for p in problems)


def test_invalid_toml_is_reported(tmp_path: Path) -> None:
    _write_project(tmp_path, "beginner", "01-broken", "this is = = not toml")
    assert any("invalid TOML" in p for p in scan_projects(tmp_path))


def test_missing_required_field_is_reported(tmp_path: Path) -> None:
    metadata = VALID_METADATA.replace(
        'summary = "Track expenses from the command line."\n', ""
    )
    _write_project(tmp_path, "beginner", "01-expense-tracker", metadata)
    assert any(
        "[summary]: missing required field" in p for p in scan_projects(tmp_path)
    )


def test_bad_level_and_status_reported(tmp_path: Path) -> None:
    metadata = VALID_METADATA.replace('level = "beginner"', 'level = "expert"').replace(
        'status = "complete"', 'status = "done"'
    )
    _write_project(tmp_path, "beginner", "01-expense-tracker", metadata)
    problems = scan_projects(tmp_path)
    assert any("[level]" in p for p in problems)
    assert any("[status]" in p for p in problems)


def test_unsupported_python_lower_bound_reported(tmp_path: Path) -> None:
    metadata = VALID_METADATA.replace('python = ">=3.12"', 'python = ">=3.10"')
    _write_project(tmp_path, "beginner", "01-expense-tracker", metadata)
    assert any("below the supported minimum" in p for p in scan_projects(tmp_path))


def test_unknown_interface_reported(tmp_path: Path) -> None:
    metadata = VALID_METADATA.replace('interfaces = ["cli"]', 'interfaces = ["gui"]')
    _write_project(tmp_path, "beginner", "01-expense-tracker", metadata)
    assert any("[interfaces]" in p for p in scan_projects(tmp_path))


def test_featured_must_be_complete(tmp_path: Path) -> None:
    metadata = VALID_METADATA.replace('status = "complete"', 'status = "draft"')
    _write_project(
        tmp_path, "beginner", "01-expense-tracker", metadata, with_tests=False
    )
    assert any(
        "only a 'complete' project may be featured" in p
        for p in scan_projects(tmp_path)
    )


def test_complete_without_tests_reported(tmp_path: Path) -> None:
    _write_project(
        tmp_path, "beginner", "01-expense-tracker", VALID_METADATA, with_tests=False
    )
    assert any("requires tests/" in p for p in scan_projects(tmp_path))


def test_folder_level_mismatch_reported(tmp_path: Path) -> None:
    # Valid metadata says beginner, but the folder is under intermediate.
    _write_project(tmp_path, "intermediate", "01-expense-tracker", VALID_METADATA)
    problems = scan_projects(tmp_path)
    assert any("does not match its folder" in p for p in problems)


def test_bad_folder_name_reported(tmp_path: Path) -> None:
    _write_project(tmp_path, "beginner", "expense-tracker", VALID_METADATA)
    assert any("[folder]" in p for p in scan_projects(tmp_path))


def test_duplicate_id_and_slug_reported(tmp_path: Path) -> None:
    _write_project(tmp_path, "beginner", "01-expense-tracker", VALID_METADATA)
    # Second project reuses the same id and slug but a different folder number.
    metadata_two = VALID_METADATA.replace("01-expense", "02-expense")
    _write_project(tmp_path, "beginner", "02-expense-tracker", metadata_two)
    problems = scan_projects(tmp_path)
    assert any("duplicate" in p for p in problems)


def test_main_valid(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_project(tmp_path, "beginner", "01-expense-tracker", VALID_METADATA)
    assert main(["--root", str(tmp_path)]) == 0
    assert "valid" in capsys.readouterr().out


def test_main_invalid(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    _write_project(
        tmp_path, "beginner", "01-expense-tracker", VALID_METADATA, with_tests=False
    )
    assert main(["--root", str(tmp_path)]) == 1
    assert "problem(s) found" in capsys.readouterr().out
