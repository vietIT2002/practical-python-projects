"""Tests for URL safety checks."""

from __future__ import annotations

import pytest

from website_change_monitor.errors import UnsafeUrlError
from website_change_monitor.safety import validate_url


def test_public_https_is_allowed() -> None:
    validate_url("https://example.com/page")  # no exception


@pytest.mark.parametrize(
    "url",
    [
        "ftp://example.com",
        "file:///etc/passwd",
        "http://localhost/",
        "http://app.localhost/",
        "http://127.0.0.1/",
        "http://10.0.0.5/",
        "http://192.168.1.1/",
        "http://169.254.1.1/",
    ],
)
def test_unsafe_urls_are_rejected(url: str) -> None:
    with pytest.raises(UnsafeUrlError):
        validate_url(url)


def test_allow_private_override() -> None:
    validate_url("http://127.0.0.1/", allow_private=True)  # no exception


def test_missing_host_rejected() -> None:
    with pytest.raises(UnsafeUrlError):
        validate_url("http://")
