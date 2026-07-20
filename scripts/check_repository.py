"""Deterministic structural checks for the repository.

These checks guard the conventions documented in ``docs/repository-map.md`` so
that a missing landing page or a mis-named project folder fails fast, locally
and in continuous integration. (Markdown links are checked separately by
``scripts/check_internal_links.py``.)

Run it from the repository root:

    python scripts/check_repository.py

The command prints one problem per line and exits non-zero if any check fails.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

#: Files that must always exist at the repository root.
REQUIRED_ROOT_FILES = ("README.md", "LICENSE", "pyproject.toml")

#: Difficulty levels; each must have a landing page.
LEVELS = ("beginner", "intermediate", "advanced")

#: Project folders are named ``NN-kebab-case-slug`` (see ADR-0003).
PROJECT_NAME = re.compile(r"^\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$")


def check_required_files(root: Path) -> list[str]:
    """Report any required root file that is missing."""
    return [
        f"missing required root file: {name}"
        for name in REQUIRED_ROOT_FILES
        if not (root / name).is_file()
    ]


def check_level_pages(root: Path) -> list[str]:
    """Report any difficulty level whose landing page is missing."""
    problems: list[str] = []
    for level in LEVELS:
        directory = root / level
        if not directory.is_dir():
            problems.append(f"missing level directory: {level}/")
        elif not (directory / "README.md").is_file():
            problems.append(f"missing landing page: {level}/README.md")
    return problems


def check_project_naming(root: Path) -> list[str]:
    """Report project folders that break the naming convention.

    A project folder is any directory directly under a level directory. Each
    must match ``NN-kebab-case-slug`` and contain a ``README.md``.
    """
    problems: list[str] = []
    for level in LEVELS:
        directory = root / level
        if not directory.is_dir():
            continue
        for child in sorted(directory.iterdir()):
            if not child.is_dir() or child.name.startswith("."):
                continue
            if not PROJECT_NAME.match(child.name):
                problems.append(
                    f"project folder does not match 'NN-slug': {level}/{child.name}"
                )
            if not (child / "README.md").is_file():
                problems.append(f"project is missing a README: {level}/{child.name}")
    return problems


def run_checks(root: Path) -> list[str]:
    """Run all structural checks and return a combined list of problems."""
    return [
        *check_required_files(root),
        *check_level_pages(root),
        *check_project_naming(root),
    ]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root to check (defaults to the repository root)",
    )
    args = parser.parse_args(argv)

    problems = run_checks(args.root)
    if problems:
        for problem in problems:
            print(problem)
        print(f"\n{len(problems)} problem(s) found.")
        return 1
    print("Repository checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
