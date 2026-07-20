"""Check repository-relative Markdown links in tracked Markdown files.

Verifies that every relative link points at a file that exists, and that any
``#anchor`` matches a heading in the target file. External links (http/https,
mailto) are intentionally ignored so a temporarily unavailable website never
makes a pull request flaky.

Usage::

    python scripts/check_internal_links.py
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

EXCLUDE_DIRS = {".git", ".venv", ".ai", "__pycache__", "node_modules"}
_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
_HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*$")


def _slug(heading: str) -> str:
    text = heading.strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text)


def _anchors(path: Path) -> set[str]:
    anchors: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = _HEADING.match(line)
        if match:
            anchors.add(_slug(match.group(1)))
    return anchors


def markdown_files(root: Path) -> list[Path]:
    return sorted(
        path
        for path in root.rglob("*.md")
        if not any(part in EXCLUDE_DIRS for part in path.relative_to(root).parts)
    )


def find_broken_links(root: Path) -> list[str]:
    """Return a list of problems, one per broken relative link or anchor."""
    problems: list[str] = []
    for markdown in markdown_files(root):
        rel = markdown.relative_to(root).as_posix()
        for target in _LINK.findall(markdown.read_text(encoding="utf-8")):
            target = target.strip()
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if target.startswith("#"):
                if _slug(target[1:]) not in _anchors(markdown):
                    problems.append(f"{rel}: missing anchor '{target}'")
                continue
            path_part, _, anchor = target.partition("#")
            if not path_part:
                continue
            destination = (markdown.parent / path_part).resolve()
            if not destination.exists():
                problems.append(f"{rel}: broken link -> '{target}'")
                continue
            if (
                anchor
                and destination.is_file()
                and destination.suffix == ".md"
                and _slug(anchor) not in _anchors(destination)
            ):
                problems.append(f"{rel}: missing anchor -> '{target}'")
    return problems


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--root", type=Path, default=Path(__file__).resolve().parents[1]
    )
    args = parser.parse_args(argv)

    problems = find_broken_links(args.root)
    if problems:
        for problem in problems:
            print(problem)
        print(f"\n{len(problems)} broken internal link(s).")
        return 1
    print(
        f"All internal Markdown links resolve ({len(markdown_files(args.root))} files)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
