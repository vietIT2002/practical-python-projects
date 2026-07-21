# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the repository
follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

_Nothing yet._

## [0.1.0] - 2026-07-21

First public release: the repository foundation and three complete launch
projects.

### Added

- **Toolchain and quality gates** — a `uv`-managed development environment with
  Ruff, mypy (strict), pytest with branch coverage, pre-commit, and a dependency
  vulnerability audit.
- **Continuous integration** across Python 3.12, 3.13, and 3.14, running
  formatting, linting, type checking, tests, repository-structure checks,
  metadata validation, internal-link checking, and a generated-catalog check.
- **Community and security files** — LICENSE (MIT), CONTRIBUTING,
  CODE_OF_CONDUCT, SECURITY, SUPPORT, GOVERNANCE, CODEOWNERS, issue forms, and a
  pull request template.
- **Visual identity and landing README** with truthful CI, license, and Python
  badges.
- **Project template and metadata** — a copyable project template and a
  machine-validated `project.toml` contract.
- **Automated project catalogs** generated from project metadata (one source of
  truth).
- **Launch projects:**
  - [Expense Tracker CLI](beginner/01-expense-tracker/README.md) — beginner.
  - [Safe File Organizer CLI](beginner/02-file-organizer/README.md) — beginner.
  - [URL Shortener API](intermediate/01-url-shortener-api/README.md) —
    intermediate.

### Known limitations

- The projects are for learning; they are not hardened for production use.
- The URL Shortener API is an intentional open redirector with no rate limiting
  or authentication (see its threat model).

> Comparison and tag links become available once `v0.1.0` is tagged; see
> [docs/releases/release-process.md](docs/releases/release-process.md).
