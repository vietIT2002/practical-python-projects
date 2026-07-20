"""Validate every project's ``project.toml`` against the metadata contract.

The contract is documented in ``docs/project-metadata.md``. This validator is
the machine-readable source of truth: it is run locally and in continuous
integration, and it rejects, for example, a project marked ``complete`` that is
missing tests.

Run it from the repository root:

    python scripts/validate_project_metadata.py

It scans the ``beginner``, ``intermediate``, and ``advanced`` directories, prints
one problem per line (with the project path, field, bad value, and how to fix
it), and exits non-zero if any project is invalid.
"""

from __future__ import annotations

import argparse
import re
import tomllib
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
LEVELS = ("beginner", "intermediate", "advanced")
STATUSES = ("draft", "complete")
INTERFACES = ("cli", "api", "library", "pipeline")

REQUIRED_FIELDS = (
    "schema_version",
    "id",
    "slug",
    "title",
    "level",
    "status",
    "summary",
    "python",
    "interfaces",
)

_ID = re.compile(r"^(beginner|intermediate|advanced)-(\d{2})$")
_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_FOLDER = re.compile(r"^(\d{2})-([a-z0-9]+(?:-[a-z0-9]+)*)$")
_PY_LOWER_BOUND = re.compile(r"^>=\s*(\d+)\.(\d+)")


def _problem(project: str, field: str, message: str) -> str:
    return f"{project} [{field}]: {message}"


def _check_types_and_values(project: str, data: dict[str, Any]) -> list[str]:
    problems: list[str] = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            problems.append(_problem(project, field, "missing required field"))

    schema_version = data.get("schema_version")
    if "schema_version" in data and schema_version != SCHEMA_VERSION:
        problems.append(
            _problem(
                project,
                "schema_version",
                f"got {schema_version!r}; expected {SCHEMA_VERSION}",
            )
        )

    for field in ("id", "slug", "title", "summary", "level", "status", "python"):
        if field in data and not isinstance(data[field], str):
            problems.append(_problem(project, field, "must be a string"))

    if isinstance(data.get("level"), str) and data["level"] not in LEVELS:
        problems.append(
            _problem(project, "level", f"got {data['level']!r}; allowed: {LEVELS}")
        )

    if isinstance(data.get("status"), str) and data["status"] not in STATUSES:
        problems.append(
            _problem(project, "status", f"got {data['status']!r}; allowed: {STATUSES}")
        )

    if isinstance(data.get("id"), str) and not _ID.match(data["id"]):
        problems.append(
            _problem(project, "id", f"got {data['id']!r}; expected e.g. 'beginner-01'")
        )

    if isinstance(data.get("slug"), str) and not _SLUG.match(data["slug"]):
        problems.append(
            _problem(project, "slug", f"got {data['slug']!r}; must be kebab-case")
        )

    problems.extend(_check_interfaces(project, data))
    problems.extend(_check_python(project, data))
    problems.extend(_check_featured(project, data))
    return problems


def _check_interfaces(project: str, data: dict[str, Any]) -> list[str]:
    if "interfaces" not in data:
        return []
    interfaces = data["interfaces"]
    if not isinstance(interfaces, list) or not all(
        isinstance(item, str) for item in interfaces
    ):
        return [_problem(project, "interfaces", "must be a list of strings")]
    unknown = [item for item in interfaces if item not in INTERFACES]
    if unknown:
        return [
            _problem(project, "interfaces", f"unknown {unknown}; allowed: {INTERFACES}")
        ]
    return []


def _check_python(project: str, data: dict[str, Any]) -> list[str]:
    python = data.get("python")
    if not isinstance(python, str):
        return []
    match = _PY_LOWER_BOUND.match(python)
    if not match:
        return [_problem(project, "python", f"got {python!r}; expected e.g. '>=3.12'")]
    major, minor = int(match.group(1)), int(match.group(2))
    if (major, minor) < (3, 12):
        return [
            _problem(
                project,
                "python",
                f"lower bound {major}.{minor} is below the supported minimum 3.12",
            )
        ]
    return []


def _check_featured(project: str, data: dict[str, Any]) -> list[str]:
    if "featured" not in data:
        return []
    featured = data["featured"]
    if not isinstance(featured, bool):
        return [_problem(project, "featured", "must be true or false")]
    if featured and data.get("status") != "complete":
        return [
            _problem(project, "featured", "only a 'complete' project may be featured")
        ]
    return []


def _check_folder_match(
    project: str, data: dict[str, Any], folder_level: str, folder_number: str, slug: str
) -> list[str]:
    problems: list[str] = []
    if isinstance(data.get("level"), str) and data["level"] != folder_level:
        problems.append(
            _problem(
                project,
                "level",
                f"{data['level']!r} does not match its folder '{folder_level}/'",
            )
        )
    if isinstance(data.get("slug"), str) and data["slug"] != slug:
        problems.append(
            _problem(
                project, "slug", f"{data['slug']!r} does not match folder slug {slug!r}"
            )
        )
    match = _ID.match(data.get("id", "")) if isinstance(data.get("id"), str) else None
    if match and (match.group(1), match.group(2)) != (folder_level, folder_number):
        problems.append(
            _problem(
                project,
                "id",
                f"{data['id']!r} does not match folder {folder_level}/{folder_number}",
            )
        )
    return problems


def _check_complete_requirements(
    project: str, data: dict[str, Any], project_dir: Path
) -> list[str]:
    if data.get("status") != "complete":
        return []
    problems: list[str] = []
    if not (project_dir / "README.md").is_file():
        problems.append(_problem(project, "status", "'complete' requires a README.md"))
    tests_dir = project_dir / "tests"
    has_tests = tests_dir.is_dir() and any(tests_dir.glob("test_*.py"))
    if not has_tests:
        problems.append(
            _problem(project, "status", "'complete' requires tests/ with test_*.py")
        )
    return problems


def validate_project(project_dir: Path, root: Path) -> tuple[list[str], dict[str, Any]]:
    """Validate one project directory. Returns (problems, parsed metadata)."""
    rel = project_dir.relative_to(root).as_posix()
    folder_match = _FOLDER.match(project_dir.name)
    folder_level = project_dir.parent.name
    metadata_path = project_dir / "project.toml"

    if not metadata_path.is_file():
        return [_problem(rel, "project.toml", "missing metadata file")], {}

    try:
        data = tomllib.loads(metadata_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as error:
        return [_problem(rel, "project.toml", f"invalid TOML: {error}")], {}

    problems = _check_types_and_values(rel, data)
    problems.extend(_check_complete_requirements(rel, data, project_dir))
    if folder_match:
        problems.extend(
            _check_folder_match(
                rel, data, folder_level, folder_match.group(1), folder_match.group(2)
            )
        )
    else:
        problems.append(
            _problem(rel, "folder", "name must be 'NN-slug', e.g. '01-expense-tracker'")
        )
    return problems, data


def scan_projects(root: Path) -> list[str]:
    """Validate every project under the level directories."""
    problems: list[str] = []
    seen_ids: dict[str, str] = {}
    seen_slugs: dict[str, str] = {}

    for level in LEVELS:
        level_dir = root / level
        if not level_dir.is_dir():
            continue
        for project_dir in sorted(level_dir.iterdir()):
            if not project_dir.is_dir() or project_dir.name.startswith("."):
                continue
            rel = project_dir.relative_to(root).as_posix()
            found, data = validate_project(project_dir, root)
            problems.extend(found)

            identifier = data.get("id")
            if isinstance(identifier, str):
                if identifier in seen_ids:
                    problems.append(
                        _problem(rel, "id", f"duplicate of {seen_ids[identifier]}")
                    )
                else:
                    seen_ids[identifier] = rel
            slug = data.get("slug")
            if isinstance(slug, str):
                if slug in seen_slugs:
                    problems.append(
                        _problem(rel, "slug", f"duplicate of {seen_slugs[slug]}")
                    )
                else:
                    seen_slugs[slug] = rel
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root to scan (defaults to the repository root)",
    )
    args = parser.parse_args(argv)

    problems = scan_projects(args.root)
    if problems:
        for problem in problems:
            print(problem)
        print(f"\n{len(problems)} metadata problem(s) found.")
        return 1
    print("Project metadata is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
