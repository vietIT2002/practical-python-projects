# Architecture decisions

These Architecture Decision Records (ADRs) capture the important structural
choices for the repository: the context, the decision, the alternatives that
were considered, and the consequences. They explain *why* the repository is
shaped the way it is.

- [ADR-0001: Repository model](ADR-0001-repository-model.md) — a root tooling
  project with independent, self-contained learning projects.
- [ADR-0002: Dependency and lockfile strategy](ADR-0002-dependency-and-lockfile-strategy.md)
  — `uv`, `pyproject.toml`, committed lockfiles, and supported Python versions.
- [ADR-0003: Project layout and metadata](ADR-0003-project-layout-and-metadata.md)
  — how project folders are named and how project metadata is recorded.
