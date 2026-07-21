# Weather CLI

Show current conditions and a short forecast from the command line, using the
free **Open-Meteo** API — **no API key required**. A realistic API-integration
project with timeouts, error handling, caching, and fully offline tests.

- **Difficulty:** intermediate
- **Estimated time:** ~5 hours
- **Prerequisites:** functions, classes, basic HTTP knowledge
- **Python:** 3.12+

## What you will learn

- Integrate a real HTTP API behind a narrow, testable client.
- Set explicit connect and read timeouts.
- Handle unknown locations, provider errors, malformed responses, and being
  offline.
- Cache responses briefly to be friendly to a free provider.
- Test network code deterministically with a mock transport (no real network).

## Features

- Look up weather by place name or by `--lat`/`--lon` coordinates.
- Current conditions plus a short daily forecast (`--days`, 1–7).
- Metric or imperial units (`--units`).
- A short-lived on-disk cache (disable with `--no-cache`).

**Non-goals:** no historical data, no severe-weather alerts, no minute-by-minute
radar.

## Demo

```text
$ python -m weather_cli "Hanoi" --days 3
Hanoi, Vietnam
Now: 30.8°C, Overcast, wind 2.3 km/h

Forecast:
  2026-07-21  26.1 to 32.0°C  Thunderstorm
  2026-07-22  26.2 to 33.8°C  Thunderstorm
  2026-07-23  24.9 to 31.4°C  Thunderstorm with slight hail
```

## Setup

This project is self-contained with its own dependencies. From this directory:

```sh
cd intermediate/02-weather-cli
uv sync
PYTHONPATH=src uv run python -m weather_cli "Hanoi"       # Linux/macOS
```

```powershell
$env:PYTHONPATH = "src"; uv run python -m weather_cli "Hanoi"   # Windows
```

## Usage

```text
python -m weather_cli [LOCATION] [--lat LAT --lon LON]
                      [--units {metric,imperial}] [--days N]
                      [--no-cache] [--cache-dir DIR]
```

## Tests and quality

From this directory:

```sh
uv run pytest --cov --cov-branch
uv run ruff check .
uv run mypy .
```

Tests never hit the network — they use an `httpx` mock transport. An optional
integration test against the real API can be added behind the `integration`
marker.

## Architecture

```text
src/weather_cli/
  __main__.py      # python -m weather_cli
  cli.py           # argument parsing, formatting, output
  client.py        # the Open-Meteo client (geocoding + forecast)
  cache.py         # a small TTL file cache
  models.py        # typed location and weather records
  units.py         # metric/imperial unit systems
  weather_codes.py # WMO weather-code descriptions
  errors.py        # the error hierarchy
```

Provider-specific HTTP is confined to `client.py`, so tests inject a mock
transport and a future provider change stays local.

## Provider and limits

- **Open-Meteo** is free for non-commercial use and needs **no API key**. Please
  read the current [Open-Meteo terms](https://open-meteo.com/en/terms).
- The client sets connect and read timeouts and caches successful responses for
  a few minutes to avoid hammering the free service.
- When offline or the provider is unreachable, the CLI reports a clear error and
  exits non-zero rather than hanging.

## Limitations

- Forecast accuracy and coverage are the provider's, not this project's.
- Geocoding returns the top match; ambiguous names may resolve to the wrong
  place — use coordinates to be precise.

## Extension challenges

1. Add an `--json` output mode for scripting.
2. Add hourly forecast support.
3. **Toward a larger project:** add a second provider behind the same client
   interface and let the user choose — a lesson in abstraction and adapters.

## Troubleshooting

- **`No module named weather_cli`** — run with `PYTHONPATH=src`.
- **`error: no location found`** — try a more specific name or use
  `--lat`/`--lon`.
- **`error: timed out` / `could not reach`** — check your connection.

## License and contributing

Released under the repository [MIT License](../../LICENSE). See
[CONTRIBUTING.md](../../CONTRIBUTING.md).
