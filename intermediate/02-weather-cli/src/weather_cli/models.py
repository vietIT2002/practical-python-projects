"""Typed location and weather records."""

from __future__ import annotations

from dataclasses import dataclass

from .units import UnitSystem


@dataclass(frozen=True)
class Location:
    name: str
    country: str
    latitude: float
    longitude: float


@dataclass(frozen=True)
class CurrentConditions:
    temperature: float
    wind_speed: float
    code: int


@dataclass(frozen=True)
class DailyForecast:
    date: str
    temp_max: float
    temp_min: float
    code: int


@dataclass(frozen=True)
class Weather:
    location: Location
    current: CurrentConditions
    daily: list[DailyForecast]
    units: UnitSystem
