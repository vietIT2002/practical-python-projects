# Website Change Monitor

Notice when a web page changes. A **one-shot** command-line tool designed to run
from cron or Task Scheduler — not an always-on daemon. It fetches responsibly,
stores only a hash and a short excerpt, and reports what changed since last time.

- **Difficulty:** intermediate
- **Estimated time:** ~5 hours
- **Prerequisites:** functions, classes, basic HTTP knowledge
- **Python:** 3.12+

> ⚠️ **Use responsibly.** Only monitor sites you are allowed to, at a
> considerate frequency. See [Responsible use](#responsible-use) below.

## What you will learn

- Fetch pages with a user agent, timeouts, a redirect cap, and a size limit.
- Normalize and hash content to detect meaningful changes.
- Persist minimal state and return meaningful exit codes for scripting.
- Reduce SSRF risk by rejecting private/loopback targets.
- Test network code deterministically with a mock transport.

## Features

- Monitor one or more URLs (arguments or a `--config` JSON file).
- One-shot run with exit codes: **0** unchanged, **10** changed, **20** a check
  failed (**2** for a setup error).
- Stores only a content hash, a short excerpt, and a timestamp — never full
  pages.
- Whitespace-normalized comparison to avoid false positives.

**Non-goals:** no always-on daemon, no email/webhook alerts by default
(a safe optional extra), no crawling of linked pages.

## Demo

```text
$ python -m website_change_monitor "https://example.com/" --state-file state.json
[changed] https://example.com/: new (first check)      # exit code 10

$ python -m website_change_monitor "https://example.com/" --state-file state.json
[unchanged] https://example.com/: no change            # exit code 0
```

Run it periodically with cron (every 6 hours, conservatively):

```cron
0 */6 * * * cd /path/to/project && PYTHONPATH=src python -m website_change_monitor --config config.json --state-file state.json
```

## Setup

Self-contained with its own dependencies. From this directory:

```sh
cd intermediate/03-website-change-monitor
uv sync
PYTHONPATH=src uv run python -m website_change_monitor "https://example.com/"
```

On Windows PowerShell use `$env:PYTHONPATH = "src"` before the command.

## Usage

```text
python -m website_change_monitor [URL ...] [--config config.json]
                                 [--state-file state.json]
                                 [--max-bytes N] [--allow-private]
```

See [`examples/config.sample.json`](examples/config.sample.json) for the config
format.

## Tests and quality

```sh
uv run pytest --cov --cov-branch
uv run ruff check .
uv run mypy .
```

Tests never touch real websites — they use an `httpx` mock transport.

## Architecture

```text
src/website_change_monitor/
  __main__.py   # python -m website_change_monitor
  cli.py        # arguments, config, output, exit codes
  monitor.py    # per-URL detection and exit-code logic
  fetcher.py    # bounded, timed HTTP fetching
  safety.py     # URL scheme and SSRF-oriented checks
  normalize.py  # whitespace normalization
  state.py      # minimal last-seen state
  errors.py     # the error hierarchy
```

## Responsible use

- **Respect each site's terms of service and `robots.txt`.** This tool does not
  fetch or parse `robots.txt` for you; check it yourself before monitoring.
- **Be gentle.** Use conservative intervals (hours, not seconds). This is a
  one-shot tool precisely so you control frequency via your scheduler.
- **Respect copyright.** Stored excerpts are short and for change detection only;
  do not redistribute fetched content.
- **Do not bypass access controls.** The tool does not defeat authentication,
  paywalls, or anti-bot measures, and you should not use it to.
- **SSRF mitigation.** Only `http`/`https` are allowed, and literal
  private/loopback/reserved IP targets (and `localhost`) are rejected. Hostnames
  are not DNS-resolved here, so this is a first line of defence, not a complete
  SSRF guard — do not point it at untrusted, user-supplied URLs in a server.

## Limitations

- Whole-page hashing: any real content change triggers "changed"; it does not
  target a specific element (a documented extension idea).
- No JavaScript rendering — it sees the server's HTML only.

## Extension challenges

1. Add a CSS-selector option to watch only part of a page.
2. Add an optional, safely-configured webhook or email notification.
3. **Toward an advanced project:** store a history of changes and expose them
   through a small API or report.

## Troubleshooting

- **Exit code 20** — a check failed (timeout, HTTP error, blocked URL); the line
  for that URL explains why.
- **`No module named website_change_monitor`** — run with `PYTHONPATH=src`.

## License and contributing

Released under the repository [MIT License](../../LICENSE). See
[CONTRIBUTING.md](../../CONTRIBUTING.md).
