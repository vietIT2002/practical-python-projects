"""Generate project catalog tables from validated ``project.toml`` files.

The project metadata is the single source of truth. This script renders catalog
tables into marked regions of several Markdown files:

    <!-- project-index:start -->
    ... generated table ...
    <!-- project-index:end -->

Only content between the markers is replaced; hand-written text is preserved.
Only ``complete`` projects appear. Output is deterministic (sorted, no
timestamps) so a second run makes no changes.

Usage::

    python scripts/generate_project_index.py           # write catalogs
    python scripts/generate_project_index.py --check    # fail if stale, no write
"""

from __future__ import annotations

import argparse
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

LEVELS = ("beginner", "intermediate", "advanced")
LEVEL_ORDER = {level: index for index, level in enumerate(LEVELS)}
LEVEL_TITLES = {
    "beginner": "Beginner",
    "intermediate": "Intermediate",
    "advanced": "Advanced",
}

START_MARKER = "<!-- project-index:start -->"
END_MARKER = "<!-- project-index:end -->"

EMPTY_NOTICE = "_No projects published in this level yet._"


class GenerationError(Exception):
    """Raised when a target file is missing its generation markers."""


@dataclass(frozen=True)
class Project:
    identifier: str
    level: str
    slug: str
    title: str
    summary: str
    readme_path: str  # repo-relative, POSIX
    folder: str


def load_projects(root: Path) -> list[Project]:
    """Load metadata for every ``complete`` project, sorted deterministically."""
    projects: list[Project] = []
    for level in LEVELS:
        level_dir = root / level
        if not level_dir.is_dir():
            continue
        for project_dir in sorted(level_dir.iterdir()):
            metadata_file = project_dir / "project.toml"
            if not project_dir.is_dir() or not metadata_file.is_file():
                continue
            data = tomllib.loads(metadata_file.read_text(encoding="utf-8"))
            if data.get("status") != "complete":
                continue
            projects.append(
                Project(
                    identifier=str(data["id"]),
                    level=str(data["level"]),
                    slug=str(data["slug"]),
                    title=str(data["title"]),
                    summary=str(data["summary"]),
                    readme_path=f"{level}/{project_dir.name}/README.md",
                    folder=project_dir.name,
                )
            )
    projects.sort(key=lambda p: (LEVEL_ORDER.get(p.level, 99), p.folder, p.title))
    return projects


def _cell(text: str) -> str:
    """Render untrusted metadata text safely inside a Markdown table cell."""
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ").strip()


def _relative_link(readme_path: str, base_dir: str) -> str:
    if base_dir in ("", "."):
        return readme_path
    return str(
        PurePosixPath(readme_path).relative_to(PurePosixPath(base_dir), walk_up=True)
    )


def render_table(projects: list[Project], base_dir: str, *, include_level: bool) -> str:
    """Render a Markdown table for the given projects, or an empty notice."""
    if not projects:
        return EMPTY_NOTICE

    if include_level:
        lines = ["| Project | Level | What you build |", "|---|---|---|"]
    else:
        lines = ["| Project | What you build |", "|---|---|"]

    for project in projects:
        link = _relative_link(project.readme_path, base_dir)
        title = f"[{_cell(project.title)}]({link})"
        if include_level:
            lines.append(f"| {title} | {project.level} | {_cell(project.summary)} |")
        else:
            lines.append(f"| {title} | {_cell(project.summary)} |")
    return "\n".join(lines)


def render_catalog(projects: list[Project], base_dir: str) -> str:
    """Render the full catalog grouped by level."""
    sections: list[str] = []
    for level in LEVELS:
        subset = [p for p in projects if p.level == level]
        sections.append(
            f"### {LEVEL_TITLES[level]}\n\n"
            + render_table(subset, base_dir, include_level=False)
        )
    return "\n\n".join(sections)


def replace_region(text: str, block: str, target: str) -> str:
    """Replace the content between the markers, preserving everything else."""
    start = text.find(START_MARKER)
    end = text.find(END_MARKER)
    if start == -1 or end == -1 or end < start:
        raise GenerationError(
            f"{target}: missing or malformed project-index markers "
            f"({START_MARKER} ... {END_MARKER})"
        )
    before = text[: start + len(START_MARKER)]
    after = text[end:]
    return f"{before}\n{block}\n{after}"


def build_outputs(root: Path) -> dict[Path, str]:
    """Compute the new full text for every target file."""
    projects = load_projects(root)
    outputs: dict[Path, str] = {}

    readme = root / "README.md"
    outputs[readme] = replace_region(
        readme.read_text(encoding="utf-8"),
        render_table(projects, ".", include_level=True),
        "README.md",
    )

    for level in LEVELS:
        path = root / level / "README.md"
        subset = [p for p in projects if p.level == level]
        outputs[path] = replace_region(
            path.read_text(encoding="utf-8"),
            render_table(subset, level, include_level=False),
            f"{level}/README.md",
        )

    catalog = root / "docs" / "project-catalog.md"
    outputs[catalog] = replace_region(
        catalog.read_text(encoding="utf-8"),
        render_catalog(projects, "docs"),
        "docs/project-catalog.md",
    )
    return outputs


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="exit non-zero if any catalog is stale; do not write files",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="repository root",
    )
    args = parser.parse_args(argv)

    outputs = build_outputs(args.root)
    stale: list[Path] = []
    for path, new_text in outputs.items():
        if path.read_text(encoding="utf-8") != new_text:
            stale.append(path)

    if args.check:
        if stale:
            for path in stale:
                print(f"stale: {path.relative_to(args.root).as_posix()}")
            print("\nRun: uv run python scripts/generate_project_index.py")
            return 1
        print("Project catalogs are up to date.")
        return 0

    for path in stale:
        # Always write LF so the output is identical on every OS.
        path.write_text(outputs[path], encoding="utf-8", newline="\n")
        print(f"updated: {path.relative_to(args.root).as_posix()}")
    if not stale:
        print("Project catalogs already up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
