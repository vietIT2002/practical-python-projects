"""Command-line interface: argument parsing, formatting, and output."""

from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path

from . import __version__
from .cache import FileCache
from .client import DEFAULT_CACHE_TTL, WeatherClient, create_http_client
from .errors import WeatherError
from .models import Location, Weather
from .units import UNIT_SYSTEMS
from .weather_codes import describe

MIN_DAYS = 1
MAX_DAYS = 7


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="weather-cli",
        description="Show current conditions and a short forecast (Open-Meteo).",
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument("location", nargs="?", help="place name, e.g. 'Hanoi'")
    parser.add_argument("--lat", type=float, help="latitude (use with --lon)")
    parser.add_argument("--lon", type=float, help="longitude (use with --lat)")
    parser.add_argument("--units", choices=sorted(UNIT_SYSTEMS), default="metric")
    parser.add_argument(
        "--days", type=int, default=3, help=f"forecast days ({MIN_DAYS}-{MAX_DAYS})"
    )
    parser.add_argument("--no-cache", action="store_true", help="disable caching")
    parser.add_argument(
        "--cache-dir",
        type=Path,
        default=Path(tempfile.gettempdir()) / "weather-cli-cache",
        help="cache directory",
    )
    return parser


def _resolve_target(args: argparse.Namespace) -> tuple[Location | None, str | None]:
    if args.lat is not None or args.lon is not None:
        if args.lat is None or args.lon is None:
            raise WeatherError("both --lat and --lon are required together")
        location = Location("custom", "", args.lat, args.lon)
        return location, None
    if not args.location:
        raise WeatherError("provide a place name or --lat/--lon")
    return None, args.location


def _format(weather: Weather) -> str:
    units = weather.units
    place = weather.location.name
    if weather.location.country:
        place += f", {weather.location.country}"
    lines = [
        f"{place}",
        f"Now: {weather.current.temperature}{units.temperature_symbol}, "
        f"{describe(weather.current.code)}, "
        f"wind {weather.current.wind_speed} {units.wind_symbol}",
        "",
        "Forecast:",
    ]
    for day in weather.daily:
        lines.append(
            f"  {day.date}  {day.temp_min} to {day.temp_max}"
            f"{units.temperature_symbol}  {describe(day.code)}"
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if not MIN_DAYS <= args.days <= MAX_DAYS:
        print(
            f"error: --days must be between {MIN_DAYS} and {MAX_DAYS}", file=sys.stderr
        )
        return 2

    units = UNIT_SYSTEMS[args.units]
    cache = None if args.no_cache else FileCache(args.cache_dir, DEFAULT_CACHE_TTL)

    try:
        location, name = _resolve_target(args)
        with create_http_client() as http:
            client = WeatherClient(http, cache)
            weather = client.get_weather(
                location=location, name=name, units=units, days=args.days
            )
    except WeatherError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(_format(weather))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
