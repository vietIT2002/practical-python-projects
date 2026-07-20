"""Command-line interface: argument parsing and input/output only.

Exit codes:

- ``0`` success (including a dry run)
- ``1`` a domain error, or a partial failure during apply
- ``2`` a usage error (handled by :mod:`argparse`)
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .classify import load_rules
from .errors import OrganizerError
from .executor import apply_plan, undo_moves
from .manifest import DEFAULT_MANIFEST_NAME, load_manifest, save_manifest
from .models import Plan
from .planner import build_plan


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="file-organizer",
        description="Safely organise files into category folders (dry run by default).",
    )
    parser.add_argument("--version", action="version", version=__version__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    organize = subparsers.add_parser(
        "organize", help="plan (and optionally apply) moves from a source directory"
    )
    organize.add_argument("source", type=Path, help="directory to organise")
    organize.add_argument("destination", type=Path, help="where category folders go")
    organize.add_argument(
        "--apply",
        action="store_true",
        help="actually move files (without this, it is a dry run)",
    )
    organize.add_argument(
        "--config", type=Path, default=None, help="JSON category configuration"
    )
    organize.add_argument(
        "--manifest",
        type=Path,
        default=None,
        help="where to write the undo manifest (default: <destination>/"
        f"{DEFAULT_MANIFEST_NAME})",
    )

    undo = subparsers.add_parser(
        "undo", help="reverse a previous apply using its manifest"
    )
    undo.add_argument("manifest", type=Path, help="manifest file from a previous apply")
    undo.add_argument(
        "--apply",
        action="store_true",
        help="actually restore files (without this, it is a dry run)",
    )

    return parser


def _print_plan(plan: Plan) -> None:
    if plan.moves:
        print(f"Planned moves ({len(plan.moves)}):")
        for move in plan.moves:
            print(f"  {move.source.name}  ->  {move.category}/{move.destination.name}")
    else:
        print("No files to move.")
    if plan.skipped:
        print(f"\nSkipped ({len(plan.skipped)}):")
        for skip in plan.skipped:
            print(f"  {skip.path.name}  ({skip.reason})")


def _run_organize(args: argparse.Namespace) -> int:
    rules = load_rules(args.config)
    plan = build_plan(args.source, args.destination, rules)
    _print_plan(plan)

    if not args.apply:
        print("\nDry run. Re-run with --apply to move files.")
        return 0

    if not plan.moves:
        return 0

    result = apply_plan(plan.moves)
    manifest_path = args.manifest or (
        args.destination.expanduser().resolve() / DEFAULT_MANIFEST_NAME
    )
    save_manifest(manifest_path, result.completed)

    print(f"\nMoved {len(result.completed)} file(s). Manifest: {manifest_path}")
    if result.failure is not None:
        pending = len(plan.moves) - len(result.completed)
        print(
            f"error: stopped after a failure on {result.failure.source.name}: "
            f"{result.error}\n{pending} move(s) were not attempted.",
            file=sys.stderr,
        )
        return 1
    return 0


def _run_undo(args: argparse.Namespace) -> int:
    moves = load_manifest(args.manifest)

    if not args.apply:
        print(f"Would restore {len(moves)} file(s):")
        for move in moves:
            print(f"  {move.destination.name}  ->  {move.source}")
        print("\nDry run. Re-run with --apply to restore files.")
        return 0

    result = undo_moves(moves)
    print(f"Restored {len(result.restored)} file(s).")
    if result.skipped:
        print(f"\nSkipped {len(result.skipped)} (unsafe or ambiguous):")
        for move, reason in result.skipped:
            print(f"  {move.destination.name}  ({reason})")
    return 0


_COMMANDS = {"organize": _run_organize, "undo": _run_undo}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = _COMMANDS[args.command]
    try:
        return handler(args)
    except OrganizerError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
