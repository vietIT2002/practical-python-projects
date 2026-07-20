# Issue and pull-request labels

A small, purposeful label set. These labels are referenced by the issue
templates (`.github/ISSUE_TEMPLATE/`) and the release-note configuration
(`.github/release.yml`), so keep the names in step with those files.

## Type

| Label | Description |
|---|---|
| `bug` | Something is broken or behaves incorrectly. |
| `enhancement` | A new feature or improvement to existing work. |
| `documentation` | Documentation additions or corrections. |
| `project-proposal` | A proposal to add a new learning project. |
| `project` | Work that adds or substantially changes a learning project. |
| `security` | Security-relevant fix or hardening. |
| `chore` | Tooling or maintenance with no user-facing behaviour change. |
| `ci` | Continuous integration or workflow changes. |
| `dependencies` | Dependency updates (also applied by Dependabot). |

## Workflow

| Label | Description |
|---|---|
| `needs-triage` | Not yet reviewed by a maintainer. |
| `good first issue` | Small, well-scoped task suitable for newcomers. |
| `help wanted` | Extra attention or contribution is welcome. |
| `blocked` | Cannot proceed until something else is resolved. |
| `ignore-for-release` | Excluded from generated release notes. |

## Guidance

- Every new issue starts with `needs-triage` (applied automatically by the
  templates) plus a type label.
- Keep `good first issue` tasks genuinely small and reproducible.
- Do not create a large backlog of vague labels to appear active.
