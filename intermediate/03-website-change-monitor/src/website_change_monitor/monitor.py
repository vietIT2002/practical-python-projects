"""Per-URL change detection and exit-code logic."""

from __future__ import annotations

import hashlib
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import Enum

import httpx

from .errors import MonitorError
from .fetcher import DEFAULT_MAX_BYTES, fetch
from .normalize import normalize
from .safety import validate_url
from .state import State

EXIT_UNCHANGED = 0
EXIT_CHANGED = 10
EXIT_FAILED = 20

_EXCERPT_LENGTH = 80


class Status(Enum):
    UNCHANGED = "unchanged"
    CHANGED = "changed"
    FAILED = "failed"


@dataclass(frozen=True)
class CheckResult:
    url: str
    status: Status
    detail: str


Clock = Callable[[], str]


def _now_iso() -> str:
    return datetime.now(UTC).isoformat()


def check_url(
    client: httpx.Client,
    url: str,
    state: State,
    *,
    allow_private: bool = False,
    max_bytes: int = DEFAULT_MAX_BYTES,
    now: Clock = _now_iso,
) -> CheckResult:
    """Check one URL, updating ``state`` on a successful fetch."""
    try:
        validate_url(url, allow_private=allow_private)
        text = fetch(client, url, max_bytes=max_bytes)
    except MonitorError as error:
        return CheckResult(url, Status.FAILED, str(error))

    normalized = normalize(text)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    previous = state.get(url)
    state[url] = {
        "hash": digest,
        "excerpt": normalized[:_EXCERPT_LENGTH],
        "checked_at": now(),
    }
    if previous is None:
        return CheckResult(url, Status.CHANGED, "new (first check)")
    if previous.get("hash") != digest:
        return CheckResult(url, Status.CHANGED, "content changed")
    return CheckResult(url, Status.UNCHANGED, "no change")


def run_checks(
    client: httpx.Client,
    urls: list[str],
    state: State,
    *,
    allow_private: bool = False,
    max_bytes: int = DEFAULT_MAX_BYTES,
    now: Clock = _now_iso,
) -> list[CheckResult]:
    return [
        check_url(
            client,
            url,
            state,
            allow_private=allow_private,
            max_bytes=max_bytes,
            now=now,
        )
        for url in urls
    ]


def exit_code_for(results: list[CheckResult]) -> int:
    """Failures take precedence over changes; unchanged is success."""
    if any(result.status is Status.FAILED for result in results):
        return EXIT_FAILED
    if any(result.status is Status.CHANGED for result in results):
        return EXIT_CHANGED
    return EXIT_UNCHANGED
