# Project plan: Weather CLI

A milestone path for integrating a real HTTP API with reliable, offline tests.

## Problem

Show the weather for a place from the command line — a realistic API-integration
exercise with timeouts, error handling, and caching.

## Milestone 1 — models and units

- Define typed location and weather records and the metric/imperial unit systems.

## Milestone 2 — the client

- Wrap Open-Meteo geocoding and forecast behind a narrow `WeatherClient`.
- Set explicit connect and read timeouts.
- Map timeouts, provider errors, and malformed responses to clear errors.

## Milestone 3 — caching

- Add a short TTL file cache to be friendly to the free provider.
- Make the clock injectable and test expiry.

## Milestone 4 — CLI

- Accept a place name or coordinates, unit choice, and forecast days.
- Format current conditions and a short forecast; use clear exit codes.

## Milestone 5 — tests and polish

- Test with a mock transport (no real network): success, units, provider error,
  malformed JSON, timeout, and cache.
- Write the README documenting the provider and its limits.

## Definition of Done

Meets the
[Project Definition of Done](../../docs/repository-map.md#draft-vs-published).
