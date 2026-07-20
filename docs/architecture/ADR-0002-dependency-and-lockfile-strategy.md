# ADR-0002: Dependency and lockfile strategy

- Date: 2026-07-20
- Status: Accepted

## Context

The repository targets learners and must remain reproducible, secure, and easy
to set up. Projects range from standard-library-only scripts to applications
with third-party runtime dependencies. We need a consistent, low-surprise
policy for declaring dependencies, locking versions, and supporting multiple
Python versions, without forcing every learner to install everything.

## Decision

- **Package and environment manager:** `uv`.
- **Declaration:** `pyproject.toml` for any project that has Python
  dependencies or is a packaged application. Runtime and development
  dependencies are separated (dependency groups / extras).
- **Standard-library beginner projects** may omit third-party runtime
  dependencies entirely and are not required to carry a `pyproject.toml`
  runtime dependency list; they still carry project metadata (see ADR-0003).
- **Lockfiles:** commit `uv.lock` for (a) the root tooling project and
  (b) each self-contained project that has third-party runtime dependencies.
  Beginner standard-library projects do not need a runtime lockfile.
- **Python support:** minimum **3.12**. CI targets **3.12, 3.13, and 3.14**,
  enabling a version only when all locked dependencies support it.
- **Version bounds:** declare meaningful lower bounds tied to real feature use;
  avoid unnecessary upper bounds; rely on the lockfile for exact
  reproducibility.
- **Updates:** Dependabot for the Python ecosystem and `github-actions`
  (configured in Phase 03/04). Lockfiles are updated with `uv`, never by hand.
  Major updates are not auto-merged.
- **Auditing:** a dependency vulnerability audit is part of release checks
  (Phase 11). Ignored advisories require a documented rationale and review date.
- **No duplicate `requirements.txt`** files unless generated for a documented
  compatibility reason.

## Alternatives considered

1. **pip + venv + requirements.txt.** Rejected as the primary flow: weaker
   reproducibility and slower; `uv` provides fast, lockfile-based installs.
2. **Poetry / PDM.** Reasonable, but `uv` is already the brief's chosen tool
   and offers a single fast toolchain for envs, locking, and running.
3. **One shared lockfile for all projects.** Rejected: see ADR-0001; harms
   isolation and forces over-installation.

## Consequences

- Positive: reproducible installs, clear runtime/dev separation, per-project
  isolation, and a single modern toolchain.
- Positive: beginner projects stay dependency-free and approachable.
- Negative: multiple lockfiles to maintain; mitigated by Dependabot and
  automation.
- Risk: Python 3.14 support depends on ecosystem readiness; CI enables a
  version only when locked dependencies support it, so the matrix may lag.

## Related decisions

- [ADR-0001: Repository model](ADR-0001-repository-model.md)
- [ADR-0003: Project layout and metadata](ADR-0003-project-layout-and-metadata.md)
