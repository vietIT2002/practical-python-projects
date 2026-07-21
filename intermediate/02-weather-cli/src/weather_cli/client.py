"""The Open-Meteo client: geocoding and forecast, behind a narrow interface.

Open-Meteo requires no API key for non-commercial use. Provider-specific details
are contained here so tests can inject a mock transport and a future provider
change stays local.
"""

from __future__ import annotations

from typing import Any

import httpx

from .cache import FileCache
from .errors import (
    LocationNotFoundError,
    OfflineError,
    ProviderError,
    ResponseError,
)
from .models import CurrentConditions, DailyForecast, Location, Weather
from .units import UnitSystem

GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

DEFAULT_TIMEOUT = httpx.Timeout(connect=5.0, read=10.0, write=10.0, pool=5.0)
DEFAULT_CACHE_TTL = 600.0  # seconds


def create_http_client(timeout: httpx.Timeout = DEFAULT_TIMEOUT) -> httpx.Client:
    """Create an httpx client with explicit connect and read timeouts."""
    return httpx.Client(timeout=timeout, headers={"User-Agent": "weather-cli/0.1"})


class WeatherClient:
    def __init__(self, http: httpx.Client, cache: FileCache | None = None) -> None:
        self._http = http
        self._cache = cache

    def _get_json(self, url: str, params: dict[str, Any]) -> Any:
        key = str(httpx.URL(url, params=params))
        if self._cache is not None:
            cached = self._cache.get(key)
            if cached is not None:
                return cached
        try:
            response = self._http.get(url, params=params)
        except httpx.TimeoutException as exc:
            raise OfflineError(f"timed out contacting {url}") from exc
        except httpx.TransportError as exc:
            raise OfflineError(f"could not reach {url}: {exc}") from exc

        if response.status_code >= 400:
            raise ProviderError(f"provider returned HTTP {response.status_code}")
        try:
            payload = response.json()
        except ValueError as exc:
            raise ResponseError("provider returned malformed JSON") from exc
        if self._cache is not None:
            self._cache.set(key, payload)
        return payload

    def geocode(self, name: str) -> Location:
        data = self._get_json(
            GEOCODING_URL,
            {"name": name, "count": 1, "language": "en", "format": "json"},
        )
        results = data.get("results") if isinstance(data, dict) else None
        if not results:
            raise LocationNotFoundError(f"no location found for {name!r}")
        try:
            top = results[0]
            return Location(
                name=str(top["name"]),
                country=str(top.get("country", "")),
                latitude=float(top["latitude"]),
                longitude=float(top["longitude"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ResponseError(f"unexpected geocoding response: {exc}") from exc

    def forecast(self, location: Location, units: UnitSystem, days: int) -> Weather:
        data = self._get_json(
            FORECAST_URL,
            {
                "latitude": location.latitude,
                "longitude": location.longitude,
                "current": "temperature_2m,wind_speed_10m,weather_code",
                "daily": "temperature_2m_max,temperature_2m_min,weather_code",
                "timezone": "auto",
                "forecast_days": days,
                "temperature_unit": units.temperature_unit,
                "wind_speed_unit": units.wind_speed_unit,
            },
        )
        try:
            current_raw = data["current"]
            current = CurrentConditions(
                temperature=float(current_raw["temperature_2m"]),
                wind_speed=float(current_raw["wind_speed_10m"]),
                code=int(current_raw["weather_code"]),
            )
            daily_raw = data["daily"]
            daily = [
                DailyForecast(
                    date=str(daily_raw["time"][index]),
                    temp_max=float(daily_raw["temperature_2m_max"][index]),
                    temp_min=float(daily_raw["temperature_2m_min"][index]),
                    code=int(daily_raw["weather_code"][index]),
                )
                for index in range(len(daily_raw["time"]))
            ]
        except (KeyError, TypeError, ValueError, IndexError) as exc:
            raise ResponseError(f"unexpected forecast response: {exc}") from exc
        return Weather(location=location, current=current, daily=daily, units=units)

    def get_weather(
        self,
        *,
        location: Location | None = None,
        name: str | None = None,
        units: UnitSystem,
        days: int,
    ) -> Weather:
        if location is None:
            if name is None:
                raise ValueError("either location or name is required")
            location = self.geocode(name)
        return self.forecast(location, units, days)
