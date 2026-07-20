# ADR-0001: Repository model

- Date: 2026-07-20
- Status: Accepted

## Context

`practical-python-projects` is a public, open-source collection of complete,
teachable Python projects. The projects differ widely in scope: some are
standard-library-only beginner scripts, others are structured applications or
services with third-party runtime dependencies (for example an HTTP API).

We need a repository model that keeps every project independently runnable and
understandable while still sharing repository-wide conventions, validation, and
contributor tooling. The choice affects onboarding, dependency isolation, CI
design, and how a learner reasons about a single project in isolation.

## Decision

Adopt a **root tooling project with independent learning projects**:

- The repository root owns shared concerns only: contributor tooling
  configuration, validation and index-generation scripts, quality gates, CI,
  and community/documentation files.
- Each learning project is self-contained and runnable on its own from a clean
  clone by following its own README.
- Beginner projects prefer the Python standard library and avoid third-party
  runtime dependencies where that keeps the lesson clear.
- Projects with third-party runtime dependencies declare and lock their own
  dependencies (see ADR-0002).
- **No single `uv` workspace / shared resolver** is used at this time. A shared
  resolver would couple unrelated projects and could force a learner to install
  every project's dependencies to run one. It may be reconsidered only if a
  written analysis later shows it improves isolation and onboarding.

## Alternatives considered

1. **Single `uv` workspace for the whole repo.** Rejected: couples unrelated
   educational projects, harms per-project isolation, and complicates the
   "clone one project and run it" experience.
2. **One repository per project.** Rejected: defeats the goal of a single
   discoverable, curated learning catalog and multiplies maintenance overhead.
3. **Shared runtime library across projects.** Rejected as a default: teaching
   examples benefit from being self-contained; shared code is allowed only for
   stable repository concerns (metadata validation, index generation), per the
   architecture standard.

## Consequences

- Positive: strong per-project isolation, clear learning boundaries, simpler
  reasoning for readers, and safer dependency management.
- Positive: the root can enforce consistency (naming, metadata, quality gates)
  without dictating each project's internal design.
- Negative: some configuration is repeated across projects; mitigated by
  templates (Phase 06) and generated indexes (Phase 10) rather than manual
  copying, honoring the "one source of truth" principle.
- Negative: CI must run checks across multiple project boundaries; addressed in
  Phase 03.

## Related decisions

- [ADR-0002: Dependency and lockfile strategy](ADR-0002-dependency-and-lockfile-strategy.md)
- [ADR-0003: Project layout and metadata](ADR-0003-project-layout-and-metadata.md)
