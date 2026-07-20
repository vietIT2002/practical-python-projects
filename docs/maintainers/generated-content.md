# Generated content

Some Markdown is generated from a single source of truth so the same data is
never copied by hand across pages.

## Project catalogs

The project tables in these files are generated from each project's
`project.toml`:

- root `README.md`
- `beginner/README.md`, `intermediate/README.md`, `advanced/README.md`
- `docs/project-catalog.md`

Only the content between these markers is generated; everything else is
hand-written and preserved:

```text
<!-- project-index:start -->
<!-- project-index:end -->
```

Only `complete` projects appear, sorted by level, then folder number, then
title.

### Commands

```sh
# Regenerate the catalogs after adding or changing a project:
uv run python scripts/generate_project_index.py

# Fail if the catalogs are stale (used in CI); does not write:
uv run python scripts/generate_project_index.py --check
```

Generation is deterministic and idempotent: running it twice makes no further
changes, and it contains no timestamps.

## Rules

- Do not hand-edit content between the markers; change the `project.toml` source
  and regenerate.
- Metadata text is treated as untrusted display content and escaped when
  rendered into tables.
- The internal link checker (`scripts/check_internal_links.py`) verifies that
  every generated link resolves.
