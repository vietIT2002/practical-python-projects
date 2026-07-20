# ADR-0003: Project layout and metadata

- Date: 2026-07-20
- Status: Accepted

## Context

The catalog will grow to many projects across skill levels. Learners and the
generated project index need a predictable location, a stable naming
convention, and a single source of truth for per-project metadata (title,
level, summary, topics, status, supported Python versions). Without a
convention, metadata drifts and the index cannot be generated reliably.

## Decision

### Directory convention

Projects live under a skill-level directory using a two-digit id and a
kebab-case slug:

```text
<level>/<two-digit-id>-<kebab-case-slug>/
```

- `level` is one of: `beginner`, `intermediate`, `advanced`.
- `two-digit-id` orders projects within a level (`01`, `02`, ...).
- `kebab-case-slug` is short, descriptive, and stable once published.

Example: `beginner/01-expense-tracker-cli/`.

### Per-project structure

Follow the complexity level in the architecture standard (A: focused script,
B: structured application, C: service/pipeline). Every project has, at minimum:

- `README.md` — value, prerequisites, setup, usage, tests, learning objectives,
  architecture, limitations, extension ideas.
- `project.toml` — project metadata (see below).
- `tests/` — real tests at happy, invalid-input, and boundary levels.

Applications add `pyproject.toml`, `uv.lock`, `src/<package>/`, and
`.env.example` as needed (ADR-0002).

### Metadata source of truth

Each project owns a single `project.toml` describing at least:

- `title`, `slug`, `level`, `summary`
- `topics` (tags for discoverability)
- `status` (`draft`, `published`)
- `python` (supported version range)
- `entrypoint` / run command reference

The project index and any derived listings are **generated** from these
`project.toml` files (Phase 10). Metadata is never hand-copied into multiple
places. Only `published` projects appear in the public catalog; a project
qualifies as `published` when it meets the Project Definition of Done.

## Alternatives considered

1. **Flat project directory with no level grouping.** Rejected: harder to
   browse and to communicate a learning path as the catalog grows.
2. **Central metadata file listing every project.** Rejected: creates a
   merge-conflict hotspot and a second source of truth; per-project
   `project.toml` keeps ownership local and is aggregated by generation.
3. **Reusing `pyproject.toml` `[tool.*]` for catalog metadata.** Rejected:
   standard-library projects may not carry a `pyproject.toml`, and catalog
   metadata is a repository concern distinct from packaging.

## Consequences

- Positive: predictable navigation, stable URLs, reliable index generation,
  and a clear bar for "published".
- Positive: adding a project is mechanical and template-driven (Phase 06).
- Negative: introduces a `project.toml` schema that must be validated;
  validation is a legitimate shared repository concern (Phase 06/10).
- Negative: renaming a slug after publication breaks links; slugs are treated
  as stable once published.

## Related decisions

- [ADR-0001: Repository model](ADR-0001-repository-model.md)
- [ADR-0002: Dependency and lockfile strategy](ADR-0002-dependency-and-lockfile-strategy.md)
