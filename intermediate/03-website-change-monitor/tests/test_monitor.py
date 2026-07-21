"""Tests for change detection and exit-code logic."""

from __future__ import annotations

from collections.abc import Callable

import httpx

from website_change_monitor.monitor import (
    EXIT_CHANGED,
    EXIT_FAILED,
    EXIT_UNCHANGED,
    CheckResult,
    Status,
    check_url,
    exit_code_for,
    run_checks,
)
from website_change_monitor.state import State

URL = "https://example.com"


def _now() -> str:
    return "2026-07-21T00:00:00+00:00"


def test_first_check_is_changed(html_client: Callable[..., httpx.Client]) -> None:
    state: State = {}
    result = check_url(html_client(body="<p>v1</p>"), URL, state, now=_now)
    assert result.status is Status.CHANGED
    assert URL in state


def test_identical_content_is_unchanged(
    html_client: Callable[..., httpx.Client],
) -> None:
    state: State = {}
    check_url(html_client(body="<p>same</p>"), URL, state, now=_now)
    result = check_url(html_client(body="<p>same</p>"), URL, state, now=_now)
    assert result.status is Status.UNCHANGED


def test_changed_content_is_detected(
    html_client: Callable[..., httpx.Client],
) -> None:
    state: State = {}
    check_url(html_client(body="<p>v1</p>"), URL, state, now=_now)
    result = check_url(html_client(body="<p>v2</p>"), URL, state, now=_now)
    assert result.status is Status.CHANGED


def test_whitespace_only_change_is_ignored(
    html_client: Callable[..., httpx.Client],
) -> None:
    state: State = {}
    check_url(html_client(body="<p>a   b</p>"), URL, state, now=_now)
    result = check_url(html_client(body="<p>a b</p>\n\n"), URL, state, now=_now)
    assert result.status is Status.UNCHANGED


def test_unsafe_url_fails(html_client: Callable[..., httpx.Client]) -> None:
    state: State = {}
    result = check_url(html_client(), "http://127.0.0.1/", state, now=_now)
    assert result.status is Status.FAILED


def test_fetch_failure_is_failed(html_client: Callable[..., httpx.Client]) -> None:
    state: State = {}
    result = check_url(html_client(status=500), URL, state, now=_now)
    assert result.status is Status.FAILED


def test_run_checks_multiple(html_client: Callable[..., httpx.Client]) -> None:
    results = run_checks(html_client(), [URL, "https://example.org"], {}, now=_now)
    assert len(results) == 2


def test_exit_codes() -> None:
    unchanged = CheckResult(URL, Status.UNCHANGED, "")
    changed = CheckResult(URL, Status.CHANGED, "")
    failed = CheckResult(URL, Status.FAILED, "")
    assert exit_code_for([]) == EXIT_UNCHANGED
    assert exit_code_for([unchanged]) == EXIT_UNCHANGED
    assert exit_code_for([unchanged, changed]) == EXIT_CHANGED
    assert exit_code_for([changed, failed]) == EXIT_FAILED
