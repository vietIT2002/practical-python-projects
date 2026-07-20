# Continuous integration

The repository's quality checks run automatically on every pull request and on
every push to `main`. The workflow is defined in
[`.github/workflows/quality.yml`](../../.github/workflows/quality.yml).

## What runs

A single job, **`quality`**, runs once per supported Python version using a
matrix. Each run performs, in order:

| Step | Command | Local equivalent |
|---|---|---|
| Lockfile is current | `uv lock --check` | same |
| Install dependencies | `uv sync --locked --group dev` | `uv sync --group dev` |
| Formatting | `uv run ruff format --check .` | same |
| Linting | `uv run ruff check .` | same |
| Type checking | `uv run mypy .` | same |
| Tests + coverage | `uv run pytest --cov --cov-branch --cov-fail-under=85` | `uv run pytest --cov --cov-branch` |
| Structure validation | `uv run python scripts/check_repository.py --full` | same |

To reproduce the full CI run locally from a clean clone:

```sh
uv sync --group dev
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run mypy .
uv run pytest --cov --cov-branch --cov-report=term-missing --cov-fail-under=85
uv run python scripts/check_repository.py --full
```

## Required status checks

The job runs across the supported Python matrix, producing these check names:

- `quality (py3.12)`
- `quality (py3.13)`
- `quality (py3.14)`

These names are stable and are the ones to require in a branch protection rule
or ruleset (a maintainer action; see
[assumptions](assumptions.md#actions-that-require-github-access)).

## Design notes

- **Permissions** are set to `contents: read` only.
- **Actions are pinned** to full commit SHAs with the human-readable version in a
  comment; Dependabot (`github-actions` ecosystem) keeps them current.
- **Concurrency** cancels superseded runs on the same ref.
- The matrix uses `fail-fast: false` so one failing Python version does not hide
  results for the others.

## Diagnosing failures

- **Formatting** — run `uv run ruff format .` to fix, then commit.
- **Linting** — run `uv run ruff check --fix .`; address anything left over.
- **Type checking** — read the mypy error; add or correct type hints.
- **Coverage below threshold** — the report lists uncovered lines; add tests for
  real behaviour rather than trivial tests to pad the number.
- **Lockfile out of date** — run `uv lock` and commit the updated `uv.lock`.
- **Structure validation** — the script prints the exact problem (for example a
  mis-named project folder); fix it as described in
  [`repository-map.md`](../repository-map.md).
- **One Python version only** — usually a dependency that does not yet support
  that version; record the evidence before adjusting the matrix.
