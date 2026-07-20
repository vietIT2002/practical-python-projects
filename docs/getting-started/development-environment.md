# Development environment

This guide sets up the repository's root development toolchain from a clean
clone. The root is a non-published tooling project (see
[ADR-0001](../architecture/ADR-0001-repository-model.md)); it owns shared
quality tooling for the collection. Individual learning projects may have their
own environments in later phases.

## Prerequisites

- **Python 3.12+** (minimum supported version is 3.12; see
  [ADR-0002](../architecture/ADR-0002-dependency-and-lockfile-strategy.md)).
- **uv** — the package and environment manager.
- **git**.

### Install uv

- **Linux / macOS:**

  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **Windows (PowerShell):**

  ```powershell
  irm https://astral.sh/uv/install.ps1 | iex
  ```

See the [uv installation docs](https://docs.astral.sh/uv/getting-started/installation/)
for alternatives.

## Set up the environment

From the repository root:

```sh
uv sync --group dev
```

This creates a local virtual environment in `.venv/` and installs the pinned
development dependencies from `uv.lock`. The lockfile is committed; never edit it
by hand — update it with `uv lock`.

## Quality commands

Run these from the repository root. They are the same checks enforced by
pre-commit and (in a later phase) continuous integration:

```sh
uv run ruff format --check .   # formatting
uv run ruff check .            # linting
uv run mypy .                  # static type checking
uv run pytest                  # tests
uv lock --check                # lockfile is up to date
uv run pip-audit               # dependency vulnerability audit
uv run python scripts/check_repository.py --full   # structure + link checks
```

These are the same checks enforced in [continuous integration](../maintainers/ci.md).

To auto-fix formatting and lint issues:

```sh
uv run ruff format .
uv run ruff check --fix .
```

## Pre-commit hooks

Install the git hooks once per clone:

```sh
uv run pre-commit install
```

Run all hooks manually across the repository:

```sh
uv run pre-commit run --all-files
```

Ruff and mypy run through `uv run` inside pre-commit, so pre-commit and the
direct quality commands always use the same tool versions.

## Toolchain versions used to generate the initial lockfile

Recorded for reproducibility (initial Phase 01 lockfile, 2026-07-20):

| Tool | Version |
|---|---|
| uv | 0.11.29 |
| Python (local) | 3.12.10 |
| ruff | 0.15.22 |
| mypy | 2.3.0 |
| pytest | 9.1.1 |
| pytest-cov | 7.1.0 |
| pre-commit | 4.6.0 |
| pip-audit | 2.10.1 |

Exact resolved versions of all dependencies are pinned in `uv.lock`.
