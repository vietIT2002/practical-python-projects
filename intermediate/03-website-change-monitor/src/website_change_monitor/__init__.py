"""A one-shot website change monitor, designed for cron or Task Scheduler.

It fetches configured pages responsibly (user agent, timeout, redirect and size
limits), normalizes the content, hashes it, and reports what changed since the
last run. It stores only a hash and a short excerpt — never full pages.

Modules:

- ``errors``    — the error hierarchy.
- ``safety``    — URL scheme and SSRF-oriented target checks.
- ``normalize`` — content normalization before hashing.
- ``fetcher``   — bounded, timed HTTP fetching.
- ``state``     — last-seen state persistence.
- ``monitor``   — the per-URL check and exit-code logic.
- ``cli``       — command-line interface.
"""

from __future__ import annotations

__version__ = "0.1.0"
