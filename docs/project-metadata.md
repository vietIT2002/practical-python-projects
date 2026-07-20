# Project metadata

Every project carries a `project.toml` file describing it in a machine-readable
way. This is the single source of truth used to validate projects and, later, to
generate the public catalog. The rules here are enforced by
[`scripts/validate_project_metadata.py`](../scripts/validate_project_metadata.py).

## Schema version 1

```toml
schema_version = 1
id = "beginner-01"
slug = "expense-tracker"
title = "Expense Tracker CLI"
level = "beginner"
status = "complete"
featured = true
summary = "Track expenses from the command line."
python = ">=3.12"
interfaces = ["cli"]
concepts = ["decimal", "csv", "validation"]
prerequisites = ["functions", "basic classes"]
tags = ["cli", "files"]
estimated_minutes = 180
```

## Required fields

| Field | Type | Rule |
|---|---|---|
| `schema_version` | integer | Must be `1`. |
| `id` | string | `"<level>-NN"`, e.g. `"beginner-01"`. Unique across the repository. |
| `slug` | string | kebab-case; must match the folder's slug. Unique across the repository. |
| `title` | string | Human-readable title. |
| `level` | string | One of `beginner`, `intermediate`, `advanced`. Must match the folder. |
| `status` | string | One of `draft`, `complete`. |
| `summary` | string | One sentence describing the project. |
| `python` | string | A lower bound such as `">=3.12"`; the bound may not be below 3.12. |
| `interfaces` | list of strings | Any of `cli`, `api`, `library`, `pipeline`. |

## Optional fields

| Field | Type | Notes |
|---|---|---|
| `featured` | boolean | Defaults to `false`. Only a `complete` project may be `featured`. |
| `concepts` | list of strings | Key ideas the project teaches. |
| `prerequisites` | list of strings | What the reader should know first. |
| `tags` | list of strings | Discoverability tags. |
| `estimated_minutes` | integer | Rough time to complete. |

## Status meaning

- **`draft`** — in progress; not part of the public catalog.
- **`complete`** — meets the
  [Definition of Done](repository-map.md#draft-vs-published). A `complete`
  project must have a `README.md` and a `tests/` directory containing at least
  one `test_*.py`. This is what "published" means in the catalog.

## Folder consistency

A project lives at `<level>/NN-<slug>/`. The validator checks that:

- `level` matches the parent directory,
- `slug` matches the folder's slug, and
- the `NN` in `id` matches the folder number.

## Validation

```sh
uv run python scripts/validate_project_metadata.py
```

Errors name the project path, the field, the bad value, and how to fix it. The
same check runs in [continuous integration](maintainers/ci.md).
