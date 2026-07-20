"""Tests for the project index generator."""

from __future__ import annotations

from pathlib import Path

import pytest

from scripts.generate_project_index import (
    EMPTY_NOTICE,
    END_MARKER,
    START_MARKER,
    GenerationError,
    Project,
    _cell,
    load_projects,
    main,
    render_table,
    replace_region,
)

_MARKERS = f"{START_MARKER}\n{END_MARKER}\n"

VALID_METADATA = """\
schema_version = 1
id = "beginner-01"
slug = "demo"
title = "Demo Project"
level = "beginner"
status = "complete"
summary = "A demo project."
python = ">=3.12"
interfaces = ["cli"]
"""


def _project(**overrides: str) -> Project:
    base = {
        "identifier": "beginner-01",
        "level": "beginner",
        "slug": "demo",
        "title": "Demo",
        "summary": "A demo.",
        "readme_path": "beginner/01-demo/README.md",
        "folder": "01-demo",
    }
    base.update(overrides)
    return Project(**base)  # type: ignore[arg-type]


def test_cell_escapes_pipe_and_newline() -> None:
    assert _cell("a | b\nc") == "a \\| b c"


def test_render_table_empty_returns_notice() -> None:
    assert render_table([], "beginner", include_level=False) == EMPTY_NOTICE


def test_render_table_builds_relative_link() -> None:
    table = render_table([_project()], "beginner", include_level=False)
    assert "[Demo](01-demo/README.md)" in table


def test_render_table_link_from_docs_walks_up() -> None:
    table = render_table([_project()], "docs", include_level=True)
    assert "(../beginner/01-demo/README.md)" in table


def test_replace_region_replaces_between_markers() -> None:
    text = f"intro\n{START_MARKER}\nold\n{END_MARKER}\nafter\n"
    result = replace_region(text, "NEW", "file.md")
    assert "NEW" in result
    assert "old" not in result
    assert result.startswith("intro")
    assert result.endswith("after\n")


def test_replace_region_missing_marker_raises() -> None:
    with pytest.raises(GenerationError, match="markers"):
        replace_region("no markers here", "NEW", "file.md")


def _make_repo(root: Path) -> None:
    (root / "README.md").write_text(f"# Root\n{_MARKERS}", encoding="utf-8")
    for level in ("beginner", "intermediate", "advanced"):
        (root / level).mkdir()
        (root / level / "README.md").write_text(
            f"# {level}\n{_MARKERS}", encoding="utf-8"
        )
    (root / "docs").mkdir()
    (root / "docs" / "project-catalog.md").write_text(
        f"# Catalog\n{_MARKERS}", encoding="utf-8"
    )
    project = root / "beginner" / "01-demo"
    project.mkdir()
    (project / "README.md").write_text("# Demo\n", encoding="utf-8")
    (project / "project.toml").write_text(VALID_METADATA, encoding="utf-8")


def test_load_projects_includes_only_complete(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    draft = tmp_path / "beginner" / "02-draft"
    draft.mkdir()
    (draft / "project.toml").write_text(
        VALID_METADATA.replace("beginner-01", "beginner-02")
        .replace('slug = "demo"', 'slug = "draft"')
        .replace('status = "complete"', 'status = "draft"'),
        encoding="utf-8",
    )
    projects = load_projects(tmp_path)
    assert [p.slug for p in projects] == ["demo"]


def test_check_mode_reports_stale_then_clean(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    _make_repo(tmp_path)
    # Before generating, the catalogs are stale.
    assert main(["--root", str(tmp_path), "--check"]) == 1
    capsys.readouterr()
    # Generate, then check passes.
    assert main(["--root", str(tmp_path)]) == 0
    capsys.readouterr()
    assert main(["--root", str(tmp_path), "--check"]) == 0


def test_generation_is_idempotent(tmp_path: Path) -> None:
    _make_repo(tmp_path)
    main(["--root", str(tmp_path)])
    readme_once = (tmp_path / "README.md").read_text(encoding="utf-8")
    main(["--root", str(tmp_path)])
    assert (tmp_path / "README.md").read_text(encoding="utf-8") == readme_once
