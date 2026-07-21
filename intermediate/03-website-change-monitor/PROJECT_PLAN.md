# Project plan: Website Change Monitor

A milestone path for a responsible, one-shot change monitor.

## Problem

Notice when a web page changes — without running a always-on service or
hammering the site. A one-shot CLI fits cron or Task Scheduler.

## Milestone 1 — safety and normalization

- Validate URL schemes and reject private/loopback targets (SSRF mitigation).
- Normalize content (collapse whitespace) so cosmetic changes are ignored.

## Milestone 2 — bounded fetching

- Fetch with a user agent, connect/read timeouts, a redirect cap, and a maximum
  response size; accept only `text/*`.
- Map failures to a clear error.

## Milestone 3 — state and detection

- Store only a hash, a short excerpt, and a timestamp per URL (never full pages).
- Compare against last-seen state to classify unchanged/changed/new.

## Milestone 4 — CLI and exit codes

- Accept URLs or a config file and a state-file path.
- Return meaningful exit codes (unchanged/changed/failed) for scripting.

## Milestone 5 — tests and polish

- Test with a mock transport: unchanged, changed, normalization, timeout,
  redirect cap, oversized, bad content type, malformed state, safe-URL policy,
  and exit codes.
- Write the README with prominent responsible-use guidance.

## Definition of Done

Meets the
[Project Definition of Done](../../docs/repository-map.md#draft-vs-published).
