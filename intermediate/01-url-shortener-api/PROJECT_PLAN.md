# Project plan: URL Shortener API

A milestone-by-milestone path for building the service. Each milestone ends in
something you can run or test.

## Problem

Long URLs are awkward to share. A shortener maps a compact code to a
destination and redirects to it — a small but realistic service that touches
API design, validation, persistence, and migrations.

## Milestone 1 — configuration and database

- Add environment-based settings with safe defaults (`settings.py`).
- Set up the SQLAlchemy engine, session factory, and declarative base.
- Define the `Link` model and an initial Alembic migration.
- Test that the migration builds the schema from an empty database.

## Milestone 2 — business logic

- Write the service: create (with alias or generated code), read, redirect.
- Generate codes with `secrets`, retrying on collisions.
- Increment clicks with a single atomic SQL statement.
- Test creation, redirect counting, and not-found handling with a real session.

## Milestone 3 — API contracts

- Define Pydantic request/response schemas, validating URL scheme, alias format,
  reserved aliases, and timezone-aware future expiries.
- Add routes for create, read, redirect, and health.
- Map domain errors to consistent `404` / `410` / `409` responses.

## Milestone 4 — tests and docs

- Test the API end to end with an isolated temporary database.
- Cover invalid input, conflicts, expiry, and health.
- Write the README, `.env.example`, and the threat model.

## Milestone 5 — packaging and polish

- Add a minimal, non-root `Dockerfile` and `.dockerignore`.
- Ensure formatting, linting, type checking, tests, and metadata validation
  all pass.

## Definition of Done

The project is complete when it meets the
[Project Definition of Done](../../docs/repository-map.md#draft-vs-published):
full README, tests at all levels, passing quality checks, and valid metadata.
