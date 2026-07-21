"""Metric and imperial unit systems."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UnitSystem:
    """Provider parameters and display symbols for a unit system."""

    name: str
    temperature_unit: str  # Open-Meteo value: celsius / fahrenheit
    wind_speed_unit: str  # Open-Meteo value: kmh / mph
    temperature_symbol: str
    wind_symbol: str


METRIC = UnitSystem("metric", "celsius", "kmh", "°C", "km/h")
IMPERIAL = UnitSystem("imperial", "fahrenheit", "mph", "°F", "mph")

UNIT_SYSTEMS = {"metric": METRIC, "imperial": IMPERIAL}
