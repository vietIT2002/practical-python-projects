"""Error hierarchy for the weather client."""

from __future__ import annotations


class WeatherError(Exception):
    """Base class for expected, user-facing errors."""


class LocationNotFoundError(WeatherError):
    """Raised when a place name cannot be resolved."""


class ProviderError(WeatherError):
    """Raised when the weather provider returns an error status."""


class ResponseError(WeatherError):
    """Raised when the provider response is malformed or missing fields."""


class OfflineError(WeatherError):
    """Raised when the provider cannot be reached (timeout or connection error)."""
