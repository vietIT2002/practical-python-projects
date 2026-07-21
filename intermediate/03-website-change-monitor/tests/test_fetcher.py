"""Tests for bounded HTTP fetching (mock transport, no real network)."""

from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

from website_change_monitor.errors import FetchError
from website_change_monitor.fetcher import fetch


def test_fetch_returns_text(html_client: Callable[..., httpx.Client]) -> None:
    assert "hello" in fetch(html_client(body="<p>hello</p>"), "https://example.com")


def test_http_error(html_client: Callable[..., httpx.Client]) -> None:
    with pytest.raises(FetchError, match="HTTP 500"):
        fetch(html_client(status=500), "https://example.com")


def test_unsupported_content_type(html_client: Callable[..., httpx.Client]) -> None:
    with pytest.raises(FetchError, match="content type"):
        fetch(html_client(content_type="application/json"), "https://example.com")


def test_oversized_response(html_client: Callable[..., httpx.Client]) -> None:
    with pytest.raises(FetchError, match="exceeded"):
        fetch(html_client(body="x" * 5000), "https://example.com", max_bytes=1000)


def test_timeout(client_from: Callable[..., httpx.Client]) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("slow")

    with pytest.raises(FetchError, match="timed out"):
        fetch(client_from(handler), "https://example.com")


def test_too_many_redirects(client_from: Callable[..., httpx.Client]) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(302, headers={"location": "https://example.com/loop"})

    client = client_from(handler, follow_redirects=True, max_redirects=1)
    with pytest.raises(FetchError, match="redirects"):
        fetch(client, "https://example.com")
