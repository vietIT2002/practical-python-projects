"""A command-line weather client using the free, key-less Open-Meteo API.

Provider-specific HTTP lives behind a narrow client so tests can inject a mock
transport and the provider can change without touching the rest of the code.

Modules:

- ``errors``        — the error hierarchy.
- ``models``        — typed location and weather records.
- ``units``         — metric/imperial unit systems.
- ``weather_codes`` — WMO weather-code descriptions.
- ``cache``         — a small time-to-live file cache.
- ``client``        — the Open-Meteo client (geocoding + forecast).
- ``cli``           — argument parsing, formatting, and output.
"""

from __future__ import annotations

__version__ = "0.1.0"
