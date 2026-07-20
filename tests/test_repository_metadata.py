"""Invariant checks for the repository's root configuration.

These guard the shared toolchain contract: if someone breaks the declared
Python support or the root project model, these tests fail fast rather than
letting the whole collection drift out of sync with the architecture decisions.
"""

from __future__ import annotations

import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_pyproject() -> dict[str, object]:
    text = (REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8")
    return tomllib.loads(text)


def test_requires_python_matches_minimum_support() -> None:
    project = _load_pyproject()["project"]
    assert isinstance(project, dict)
    assert project["requires-python"] == ">=3.12"


def test_python_version_file_matches_minimum() -> None:
    pinned = (REPO_ROOT / ".python-version").read_text(encoding="utf-8").strip()
    assert pinned == "3.12"


def test_root_is_a_non_package_tooling_project() -> None:
    tool = _load_pyproject()["tool"]
    assert isinstance(tool, dict)
    uv_config = tool["uv"]
    assert isinstance(uv_config, dict)
    assert uv_config["package"] is False
