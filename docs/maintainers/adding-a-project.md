# Adding a project

The full workflow for taking a project from idea to the published catalog.

## 1. Propose

Open a **New project proposal** issue so the scope, level, and dependencies can
be agreed before implementation.

## 2. Create the folder

Choose the level and the next free two-digit number, then create:

```text
<level>/NN-<slug>/
```

Copy the template files from [`templates/project/`](../../templates/project/):

| Template | Copy to | Notes |
|---|---|---|
| `project.template.toml` | `project.toml` | Fill in every value. |
| `README.template.md` | `README.md` | Follow the section structure. |
| `test_example.template.py` | `tests/test_<name>.py` | Adapt to real behaviour. |
| `PROJECT_PLAN.template.md` | `PROJECT_PLAN.md` | Optional planning note. |
| `pyproject.template.toml` | `pyproject.toml` | Only if the project uses third-party packages. |

Standard-library-only beginner projects do not need a `pyproject.toml`.

## 3. Build it

- Keep logic separated from the interface where it helps testing.
- Make destructive actions safe by default (preview or confirmation).
- Write tests for happy-path, invalid-input, and boundary behaviour.
- Keep the metadata `status = "draft"` while you work.

## 4. Validate locally

```sh
uv run ruff format --check .
uv run ruff check .
uv run mypy .
uv run pytest --cov --cov-branch
uv run python scripts/check_repository.py --full
uv run python scripts/validate_project_metadata.py
```

## 5. Mark complete

When the project meets the
[Definition of Done](../repository-map.md#draft-vs-published), set
`status = "complete"` in `project.toml`. The validator will then require a
`README.md` and real tests.

## 6. Open a pull request

Follow the [contributing guide](../../CONTRIBUTING.md) and the pull request
template. A maintainer reviews for correctness, learning value, tests, and
documentation before it is merged and listed in the catalog.
