# Continuous integration

The repository's quality checks run automatically on every pull request and on
every push to `main`. The workflow is defined in
[`.github/workflows/quality.yml`](../../.github/workflows/quality.yml).

## What runs

The root **`quality`** job runs once per supported Python version using a
matrix. Each run performs, in order:

| Step | Command | Local equivalent |
|---|---|---|
| Lockfile is current | `uv lock --check` | same |
| Install dependencies | `uv sync --locked --group dev` | `uv sync --group dev` |
| Formatting | `uv run ruff format --check .` | same |
| Linting | `uv run ruff check .` | same |
| Type checking | `uv run mypy .` | same |
| Tests + coverage | `uv run pytest --cov --cov-branch --cov-fail-under=85` | `uv run pytest --cov --cov-branch` |
| Structure validation | `uv run python scripts/check_repository.py` | same |
| Metadata validation | `uv run python scripts/validate_project_metadata.py` | same |
| Internal links | `uv run python scripts/check_internal_links.py` | same |
| Generated catalogs current | `uv run python scripts/generate_project_index.py --check` | same |

To reproduce the root CI job locally from a clean clone:

```sh
uv sync --group dev
uv lock --check
uv run ruff format --check .
uv run ruff check .
uv run mypy .
uv run pytest --cov --cov-branch --cov-report=term-missing --cov-fail-under=85
uv run python scripts/check_repository.py
uv run python scripts/validate_project_metadata.py
uv run python scripts/check_internal_links.py
uv run python scripts/generate_project_index.py --check
```

Self-contained projects (their own dependencies) run their checks in a separate
job from their own directory. For example, the URL Shortener API:

```sh
cd intermediate/01-url-shortener-api
uv sync --group dev
uv run ruff format --check . && uv run ruff check . && uv run mypy .
uv run alembic upgrade head
uv run pytest --cov --cov-branch
```

## Required status checks

The workflow has two jobs, each across the supported Python matrix, producing
these stable check names:

- `quality (py3.12)`, `quality (py3.13)`, `quality (py3.14)`
- `url-shortener-api (py3.12)`, `url-shortener-api (py3.13)`,
  `url-shortener-api (py3.14)`

These are the checks required by the `main` branch protection rule (a maintainer
action; see [GitHub settings](github-settings.md)).

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
