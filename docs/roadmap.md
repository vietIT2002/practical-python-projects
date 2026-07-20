# Roadmap

This roadmap maps the phased build to measurable outcomes. Phases run one at a
time; each ends in a reviewable, valid repository state. The near-term goal is
`v0.1.0` (Phases 00–11) with three complete launch projects.

## Foundation

| Phase | Title | Measurable outcome |
|---:|---|---|
| 00 | Discovery and architecture | ADR-0001/0002/0003 accepted; roadmap and assumptions recorded; blockers listed. No code added. |
| 01 | Foundation and toolchain | Root `pyproject.toml` + `uv.lock`; Ruff, mypy, pytest, pytest-cov, pre-commit configured and runnable locally. |
| 02 | Repository structure and navigation | Level directories and navigation docs exist; project layout convention (ADR-0003) is realized without empty placeholder trees. |
| 03 | Quality gates and CI | GitHub Actions run lint, type check, tests, and coverage on the 3.12–3.14 matrix (as supported); Dependabot configured. |

## Open source readiness

| Phase | Title | Measurable outcome |
|---:|---|---|
| 04 | GitHub community and security | LICENSE (MIT), CONTRIBUTING, CODE_OF_CONDUCT, SECURITY, issue/PR templates present. Contact-dependent items resolved or explicitly blocked. |
| 05 | Brand, README, and discoverability | Root README explains value, path, and usage with no fake badges/metrics; discoverability plan documented (topics as maintainer actions). |
| 06 | Project template and metadata | Reusable project template plus `project.toml` schema and validation; adding a project is mechanical. |

## Launch content

| Phase | Title | Measurable outcome |
|---:|---|---|
| 07 | Expense Tracker CLI | Complete, tested CLI project passing all quality gates and Project DoD. |
| 08 | Safe File Organizer CLI | Complete, tested CLI with safe-by-default destructive operations (dry-run/confirm). |
| 09 | URL Shortener API | Complete, tested HTTP API following layered architecture and API design rules. |

## First release

| Phase | Title | Measurable outcome |
|---:|---|---|
| 10 | Project index and doc automation | Catalog/index generated from `project.toml` sources; no manually duplicated metadata. |
| 11 | Release v0.1.0 preparation | Release checklist satisfied; changelog, versioning, and dependency audit complete; release steps requiring GitHub are documented as maintainer actions. |

## Expansion

| Phase | Title | Measurable outcome |
|---:|---|---|
| 12 | Beginner project expansion | Additional beginner projects added via the template, each meeting DoD. |
| 13 | Intermediate project expansion | Intermediate projects added, each meeting DoD. |
| 14 | Advanced flagship projects | Advanced projects added, each meeting DoD. |

## Sustainable growth

| Phase | Title | Measurable outcome |
|---:|---|---|
| 15 | Community growth and maintenance | Ethical growth plan, issue backlog, and maintenance cadence documented; no metric manipulation. |
| 16 | Final v1.0 readiness audit | Full audit against launch checklist; all quality gates green; v1.0 readiness recorded. |

## Guiding constraints

- One phase at a time; small, reviewable changes.
- Evidence over confidence: report PASS / FAIL / NOT RUN honestly.
- No fake badges, metrics, or manipulated discoverability.
- Remote GitHub settings are prepared as documented maintainer actions unless
  authenticated access and explicit permission exist.
