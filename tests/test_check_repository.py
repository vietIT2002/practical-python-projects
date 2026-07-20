"""Tests for the repository validation script."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.check_repository import (
    LEVELS,
    check_markdown_links,
    check_project_naming,
    main,
    run_checks,
)


def _make_valid_repo(root: Path) -> None:
    """Create a minimal repository tree that passes every structural check."""
    (root / "README.md").write_text("# Root\n", encoding="utf-8")
    (root / "LICENSE").write_text("MIT\n", encoding="utf-8")
    (root / "pyproject.toml").write_text("[project]\nname = 'x'\n", encoding="utf-8")
    for level in LEVELS:
        (root / level).mkdir()
        (root / level / "README.md").write_text(f"# {level}\n", encoding="utf-8")


def test_valid_repository_has_no_problems(tmp_path: Path) -> None:
    _make_valid_repo(tmp_path)
    assert run_checks(tmp_path) == []


def test_missing_required_file_is_reported(tmp_path: Path) -> None:
    _make_valid_repo(tmp_path)
    (tmp_path / "LICENSE").unlink()
    problems = run_checks(tmp_path)
    assert any("LICENSE" in problem for problem in problems)


def test_missing_level_directory_is_reported(tmp_path: Path) -> None:
    _make_valid_repo(tmp_path)
    readme = tmp_path / "beginner" / "README.md"
    readme.unlink()
    (tmp_path / "beginner").rmdir()
    problems = run_checks(tmp_path)
    assert any("missing level directory: beginner/" in problem for problem in problems)


def test_missing_level_landing_page_is_reported(tmp_path: Path) -> None:
    _make_valid_repo(tmp_path)
    (tmp_path / "advanced" / "README.md").unlink()
    problems = run_checks(tmp_path)
    assert any("advanced/README.md" in problem for problem in problems)


def test_badly_named_project_folder_is_reported(tmp_path: Path) -> None:
    _make_valid_repo(tmp_path)
    bad = tmp_path / "beginner" / "MyProject"
    bad.mkdir()
    (bad / "README.md").write_text("# p\n", encoding="utf-8")
    problems = check_project_naming(tmp_path)
    assert any("does not match 'NN-slug'" in problem for problem in problems)


def test_well_named_project_without_readme_is_reported(tmp_path: Path) -> None:
    _make_valid_repo(tmp_path)
    (tmp_path / "beginner" / "01-good-slug").mkdir()
    problems = check_project_naming(tmp_path)
    assert any("missing a README" in problem for problem in problems)


def test_well_named_project_with_readme_passes(tmp_path: Path) -> None:
    _make_valid_repo(tmp_path)
    project = tmp_path / "beginner" / "01-good-slug"
    project.mkdir()
    (project / "README.md").write_text("# ok\n", encoding="utf-8")
    assert check_project_naming(tmp_path) == []


def test_full_mode_detects_broken_markdown_link(tmp_path: Path) -> None:
    _make_valid_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "See [missing](docs/nope.md) and [ok](LICENSE).\n", encoding="utf-8"
    )
    assert check_markdown_links(tmp_path)
    assert any("broken link" in problem for problem in run_checks(tmp_path, full=True))


def test_full_mode_ignores_external_and_anchor_links(tmp_path: Path) -> None:
    _make_valid_repo(tmp_path)
    (tmp_path / "README.md").write_text(
        "[web](https://example.com) [top](#intro) [mail](mailto:a@b.c)\n",
        encoding="utf-8",
    )
    assert check_markdown_links(tmp_path) == []


def test_main_returns_zero_on_valid_repo(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _make_valid_repo(tmp_path)
    exit_code = main(["--root", str(tmp_path)])
    assert exit_code == 0
    assert "passed" in capsys.readouterr().out


def test_main_returns_one_and_lists_problems(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _make_valid_repo(tmp_path)
    (tmp_path / "README.md").unlink()
    exit_code = main(["--root", str(tmp_path)])
    assert exit_code == 1
    assert "problem(s) found" in capsys.readouterr().out
