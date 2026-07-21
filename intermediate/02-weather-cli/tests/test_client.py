"""Tests for the Open-Meteo client using a mock transport (no real network)."""

from __future__ import annotations

from collections.abc import Callable

import httpx
import pytest

from weather_cli.client import WeatherClient
from weather_cli.errors import (
    LocationNotFoundError,
    OfflineError,
    ProviderError,
    ResponseError,
)
from weather_cli.models import Location
from weather_cli.units import IMPERIAL, METRIC

GEO_OK = {
    "results": [
        {"name": "Hanoi", "country": "Vietnam", "latitude": 21.03, "longitude": 105.85}
    ]
}
FORECAST_OK = {
    "current": {"temperature_2m": 30.1, "wind_speed_10m": 12.0, "weather_code": 2},
    "daily": {
        "time": ["2026-07-21", "2026-07-22"],
        "temperature_2m_max": [33.0, 34.0],
        "temperature_2m_min": [26.0, 27.0],
        "weather_code": [3, 61],
    },
}


def _client(handler: Callable[[httpx.Request], httpx.Response]) -> WeatherClient:
    http = httpx.Client(transport=httpx.MockTransport(handler))
    return WeatherClient(http, cache=None)


def _route(request: httpx.Request) -> httpx.Response:
    if request.url.path.endswith("/search"):
        return httpx.Response(200, json=GEO_OK)
    return httpx.Response(200, json=FORECAST_OK)


def test_geocode_success() -> None:
    location = _client(_route).geocode("Hanoi")
    assert location.name == "Hanoi"
    assert location.latitude == 21.03


def test_geocode_not_found() -> None:
    handler = lambda request: httpx.Response(200, json={"results": []})  # noqa: E731
    with pytest.raises(LocationNotFoundError):
        _client(handler).geocode("Nowhereville")


def test_forecast_parses_current_and_daily() -> None:
    location = Location("Hanoi", "Vietnam", 21.03, 105.85)
    weather = _client(_route).forecast(location, METRIC, days=2)
    assert weather.current.temperature == 30.1
    assert len(weather.daily) == 2
    assert weather.daily[1].code == 61


def test_units_are_sent_to_provider() -> None:
    seen: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        seen.update(dict(request.url.params))
        return httpx.Response(200, json=FORECAST_OK)

    location = Location("X", "", 1.0, 2.0)
    _client(handler).forecast(location, IMPERIAL, days=1)
    assert seen["temperature_unit"] == "fahrenheit"
    assert seen["wind_speed_unit"] == "mph"


def test_provider_error() -> None:
    handler = lambda request: httpx.Response(503)  # noqa: E731
    with pytest.raises(ProviderError, match="503"):
        _client(handler).geocode("Hanoi")


def test_malformed_json() -> None:
    handler = lambda request: httpx.Response(200, text="not json")  # noqa: E731
    with pytest.raises(ResponseError, match="malformed"):
        _client(handler).geocode("Hanoi")


def test_missing_fields_is_response_error() -> None:
    handler = lambda request: httpx.Response(200, json={"results": [{}]})  # noqa: E731
    with pytest.raises(ResponseError):
        _client(handler).geocode("Hanoi")


def test_timeout_becomes_offline_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectTimeout("timed out")

    with pytest.raises(OfflineError):
        _client(handler).geocode("Hanoi")


def test_connect_error_becomes_offline_error() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no route")

    with pytest.raises(OfflineError):
        _client(handler).geocode("Hanoi")


def test_cache_serves_second_call(tmp_path: object) -> None:
    from pathlib import Path

    from weather_cli.cache import FileCache

    calls = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        calls["n"] += 1
        return httpx.Response(200, json=GEO_OK)

    cache = FileCache(Path(str(tmp_path)), ttl_seconds=600)
    http = httpx.Client(transport=httpx.MockTransport(handler))
    client = WeatherClient(http, cache=cache)
    client.geocode("Hanoi")
    client.geocode("Hanoi")
    assert calls["n"] == 1  # second call served from cache


def test_get_weather_requires_name_or_location() -> None:
    with pytest.raises(ValueError, match="location or name"):
        _client(_route).get_weather(units=METRIC, days=1)
