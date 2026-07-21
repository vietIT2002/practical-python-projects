"""Command-line interface: one-shot check suitable for cron or Task Scheduler.

Exit codes:

- ``0``  all monitored pages unchanged
- ``10`` at least one page changed
- ``20`` at least one check failed
- ``2``  setup/usage error (bad config or state) before any check ran
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .errors import ConfigError, MonitorError
from .fetcher import DEFAULT_MAX_BYTES, create_http_client
from .monitor import exit_code_for, run_checks
from .state import load_state, save_state

DEFAULT_STATE_FILE = Path("monitor-state.json")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="website-change-monitor",
        description="Detect changes to configured web pages (one-shot, for cron).",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("urls", nargs="*", help="URLs to check")
    parser.add_argument(
        "--config", type=Path, default=None, help="JSON file with a 'urls' list"
    )
    parser.add_argument(
        "--state-file", type=Path, default=DEFAULT_STATE_FILE, help="state file path"
    )
    parser.add_argument(
        "--allow-private",
        action="store_true",
        help="allow private/loopback targets (for local testing only)",
    )
    parser.add_argument(
        "--max-bytes", type=int, default=DEFAULT_MAX_BYTES, help="max response bytes"
    )
    return parser


def _load_config_urls(path: Path) -> list[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"config not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or not isinstance(data.get("urls"), list):
        raise ConfigError(f"{path} must be an object with a 'urls' list")
    return [str(url) for url in data["urls"]]


def gather_urls(args: argparse.Namespace) -> list[str]:
    urls = list(args.urls)
    if args.config is not None:
        urls += _load_config_urls(args.config)
    if not urls:
        raise ConfigError("provide one or more URLs or a --config file")
    seen: set[str] = set()
    unique: list[str] = []
    for url in urls:
        if url not in seen:
            seen.add(url)
            unique.append(url)
    return unique


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        urls = gather_urls(args)
        state = load_state(args.state_file)
    except MonitorError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    with create_http_client() as http:
        results = run_checks(
            http,
            urls,
            state,
            allow_private=args.allow_private,
            max_bytes=args.max_bytes,
        )
    save_state(args.state_file, state)

    for result in results:
        print(f"[{result.status.value}] {result.url}: {result.detail}")
    return exit_code_for(results)


if __name__ == "__main__":
    raise SystemExit(main())
