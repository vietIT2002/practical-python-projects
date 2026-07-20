# Contributing

Thank you for your interest in improving **Practical Python Projects**. This
guide explains how to propose changes, add a project, and get a pull request
merged.

By participating, you agree to follow our [Code of Conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

- Fix a bug or improve documentation in an existing project.
- Improve the repository tooling or the contributor experience.
- Propose and build a new learning project.

If you are unsure where to start, open an issue to discuss your idea before
writing code.

## Set up your environment

Follow the
[development environment guide](docs/getting-started/development-environment.md).
In short:

```sh
uv sync --group dev
uv run pre-commit install
```

## Make your change

1. Create a short-lived branch from `main`:
   `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, or `chore/<topic>`.
2. Make the smallest coherent change that solves the problem.
3. Add or update tests for any behaviour change.
4. Keep documentation in step with the code.

## Run the checks

Your change must pass the same checks as continuous integration:

```sh
uv run ruff format --check .
uv run ruff check .
uv run mypy .
uv run pytest --cov --cov-branch
uv run python scripts/check_repository.py
uv run python scripts/validate_project_metadata.py
uv run python scripts/check_internal_links.py
uv run python scripts/generate_project_index.py --check
```

If you add or change a project, regenerate the catalogs with
`uv run python scripts/generate_project_index.py`.

Auto-fix formatting and lint issues with `uv run ruff format .` and
`uv run ruff check --fix .`.

## Proposing a new project

1. Open a **New project proposal** issue so the scope can be discussed first.
2. Copy the template from [`templates/project/`](templates/project/) and follow
   the full workflow in
   [adding a project](docs/maintainers/adding-a-project.md). Project metadata
   must follow the [metadata contract](docs/project-metadata.md).
3. A project is considered complete only when it meets the
   [draft vs published](docs/repository-map.md#draft-vs-published) bar: a full
   README, tests for happy-path, invalid-input, and boundary behaviour, and
   passing quality checks.

## Open a pull request

- Use conventional commit messages (`feat:`, `fix:`, `docs:`, `test:`,
  `refactor:`, `chore:`, `ci:`, `security:`).
- Fill in the pull request template: problem, solution, validation performed,
  and compatibility, security, and documentation effects.
- Keep pull requests small enough to review well.

A maintainer will review for correctness, clarity, tests, documentation, and
learning value, and will distinguish blocking issues from optional suggestions.

## Reporting security issues

Please do **not** open a public issue for security problems. See
[SECURITY.md](SECURITY.md) for the private reporting route.
