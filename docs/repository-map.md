# Repository map

Where everything lives, how projects are named, and what "published" means.

## Directory layout

| Path | Contents |
|---|---|
| `beginner/`, `intermediate/`, `advanced/` | Learning projects, grouped by difficulty. Each project is a self-contained folder. |
| `docs/` | Documentation: getting started, learning paths, this map, the roadmap, architecture decisions, and maintainer notes. |
| `docs/architecture/` | Architecture Decision Records (the "why" behind the structure). |
| `docs/getting-started/` | Environment setup and quality-command reference. |
| `docs/maintainers/` | Operational notes for maintainers. |
| `tests/` | Tests for the repository's own tooling and shared invariants. |
| `pyproject.toml`, `uv.lock` | The root tooling project: shared development dependencies and configuration. |
| `.pre-commit-config.yaml` | Git hooks that run the same checks as the quality commands. |
| `LICENSE` | The repository license (MIT). |

Individual projects that use third-party packages carry their own
`pyproject.toml` and `uv.lock`, so each project installs and runs on its own.

## Where quality standards live

There is no separate "standards" folder. The repository's quality bar is
expressed directly in tooling and documentation:

- **Formatting, linting, and typing** — configured in `pyproject.toml`
  (Ruff and mypy) and enforced by `.pre-commit-config.yaml`.
- **Testing** — pytest configuration in `pyproject.toml`.
- **Structural decisions** — the [architecture decisions](architecture/README.md).
- **Setup and commands** — the
  [development environment guide](getting-started/development-environment.md).

## Project naming and numbering

Each project folder is named:

```text
<level>/<two-digit-id>-<kebab-case-slug>/
```

- `level` is `beginner`, `intermediate`, or `advanced`.
- `two-digit-id` orders projects within a level (`01`, `02`, …).
- `kebab-case-slug` is short, descriptive, and stays stable once published, so
  links do not break.

Example: `beginner/01-expense-tracker-cli/`.

## Draft vs published

A project is **published** (listed in a level page and counted as part of the
catalog) only when it:

- has a complete README covering setup, usage, tests, and limitations,
- includes tests for happy-path, invalid-input, and boundary behaviour,
- passes the formatting, linting, type-checking, and test checks, and
- runs from the documented commands on a clean clone.

Anything that does not yet meet this bar is a **draft**: it may exist on a
branch or be in progress, but it is not listed as an available project.

## Generated content

When automatically generated content is introduced (for example a project
index), it will be produced by a committed script and clearly marked, so
maintainers never edit generated sections by hand.
