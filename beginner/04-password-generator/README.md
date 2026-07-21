# Secure Password Generator

Generate strong random passwords from the command line. A small project that
shows how to use cryptographically secure randomness and how to satisfy a
character-group policy without fragile "generate and retry" loops.

- **Difficulty:** beginner
- **Estimated time:** ~2 hours
- **Prerequisites:** functions
- **Python:** 3.12+ (standard library only)

## What you will learn

- Use `secrets` (not `random`) for security-sensitive values.
- Guarantee that each selected character group appears, by construction.
- Validate a policy and reject impossible or out-of-range requests.
- Shuffle securely with a Fisher–Yates using `secrets.randbelow`.
- Keep secrets out of logs and diagnostics.

## Features

- `--length` (4–256) and `--count` options.
- Toggle character groups: `--no-lowercase`, `--no-uppercase`, `--no-digits`,
  and `--symbols` (symbols are off by default).
- Every selected group is guaranteed to appear at least once.
- Impossible policies (no groups, bad length) are rejected with a clear message.

**Non-goals:** no clipboard integration, no password storage, no strength meter.

## Demo

```text
$ python -m password_generator --length 16 --symbols --count 2
q7!Kd2p@Rf9wLx#T
V3m$Zb8nH^t1Qy6s
```

(Your output will differ — the values are random.)

## Setup

Standard library only — any Python 3.12+ works. From this directory:

```sh
cd beginner/04-password-generator
PYTHONPATH=src python -m password_generator --help      # Linux/macOS
```

```powershell
$env:PYTHONPATH = "src"; python -m password_generator --help   # Windows
```

## Usage

```text
python -m password_generator [--length N] [--count N]
                             [--no-lowercase] [--no-uppercase]
                             [--no-digits] [--symbols]
```

## Tests and quality

From the repository root:

```sh
uv run pytest beginner/04-password-generator/tests
uv run ruff check .
uv run mypy .
```

## Architecture

```text
src/password_generator/
  __main__.py   # python -m password_generator
  cli.py        # command-line interface (prints to stdout only)
  generator.py  # secure generation and shuffle
  policy.py     # the policy and its validation
  errors.py     # PolicyError
```

## Key decisions

- **`secrets`, always.** Passwords must not be predictable, so generation uses
  `secrets`, never `random`.
- **Guarantee by construction.** One character is drawn from every selected
  group first, the rest from the combined pool, then the result is shuffled
  securely — no biased retry loop.
- **No leakage.** Generated passwords are printed to stdout only; they are never
  logged or echoed in diagnostics.

## Security and limitations

A generator only creates a strong password — it **does not protect it
afterwards**. Once generated, a password is only as safe as where you store it.
Use a reputable **password manager** to store and autofill passwords (several
good free and open-source options exist; this project does not endorse any paid
product). Never paste passwords into logs, chat, or untrusted tools.

The excluded symbol set avoids quotes, backslashes, spaces, and backticks so
output is safe to paste into shells and CSV; some sites may reject certain
symbols, in which case use `--no-symbols` behaviour (omit `--symbols`).

## Extension challenges

1. Add a `--exclude-ambiguous` option to drop easily confused characters
   (`O`/`0`, `l`/`1`).
2. Add a passphrase mode that joins random words from a bundled word list.
3. **Toward an intermediate project:** build a small local secrets vault with
   encryption-at-rest — a natural step up in security engineering.

## Troubleshooting

- **`No module named password_generator`** — set `PYTHONPATH=src`, or run from
  the repository root with `uv run`.
- **`error: length must be between 4 and 256`** — choose a length in range.

## License and contributing

Released under the repository [MIT License](../../LICENSE). See
[CONTRIBUTING.md](../../CONTRIBUTING.md).
