"""CLI tests with the HTTP client mocked (no real network)."""

from __future__ import annotations

import httpx
import pytest

from weather_cli import cli

GEO_OK = {
    "results": [
        {"name": "Hanoi", "country": "Vietnam", "latitude": 21.03, "longitude": 105.85}
    ]
}
FORECAST_OK = {
    "current": {"temperature_2m": 30.1, "wind_speed_10m": 12.0, "weather_code": 2},
    "daily": {
        "time": ["2026-07-21"],
        "temperature_2m_max": [33.0],
        "temperature_2m_min": [26.0],
        "weather_code": [3],
    },
}


def _route(request: httpx.Request) -> httpx.Response:
    if request.url.path.endswith("/search"):
        return httpx.Response(200, json=GEO_OK)
    return httpx.Response(200, json=FORECAST_OK)


@pytest.fixture(autouse=True)
def _mock_http(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        cli,
        "create_http_client",
        lambda: httpx.Client(transport=httpx.MockTransport(_route)),
    )


def test_by_name(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Hanoi", "--no-cache", "--days", "1"]) == 0
    out = capsys.readouterr().out
    assert "Hanoi" in out
    assert "Forecast:" in out


def test_by_coordinates(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--lat", "21.0", "--lon", "105.8", "--no-cache"]) == 0


def test_incomplete_coordinates_error(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["--lat", "21.0", "--no-cache"]) == 1
    assert "error" in capsys.readouterr().err


def test_invalid_days_usage_error(capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["Hanoi", "--days", "99"]) == 2
    assert "days must be between" in capsys.readouterr().err


def test_location_not_found(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        cli,
        "create_http_client",
        lambda: httpx.Client(
            transport=httpx.MockTransport(
                lambda request: httpx.Response(200, json={"results": []})
            )
        ),
    )
    assert cli.main(["Nowhereville", "--no-cache"]) == 1
    assert "error" in capsys.readouterr().err
