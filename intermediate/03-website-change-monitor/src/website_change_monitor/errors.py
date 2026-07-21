"""Error hierarchy for the website change monitor."""

from __future__ import annotations


class MonitorError(Exception):
    """Base class for expected, user-facing errors."""


class ConfigError(MonitorError):
    """Raised when the configuration is missing or invalid."""


class UnsafeUrlError(MonitorError):
    """Raised when a URL is not allowed (bad scheme or private/loopback target)."""


class FetchError(MonitorError):
    """Raised when a page cannot be fetched within the configured limits."""


class StateError(MonitorError):
    """Raised when the state file is malformed."""
