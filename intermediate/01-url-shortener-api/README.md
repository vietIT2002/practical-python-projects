# URL Shortener API

A small HTTP API that creates short links and redirects to their destinations,
built with FastAPI and SQLAlchemy. It shows how to design an API, validate
input, persist data with migrations, and test with isolated databases — while
being honest about its production limitations.

- **Difficulty:** intermediate
- **Estimated time:** ~7 hours
- **Prerequisites:** functions, classes, basic HTTP knowledge
- **Python:** 3.12+

## What you will learn

- Build and validate an HTTP API with FastAPI and Pydantic.
- Separate API contracts, application logic, and persistence into layers.
- Use SQLAlchemy 2.0-style models and Alembic migrations.
- Manage configuration from the environment with safe defaults.
- Test an API against an isolated temporary SQLite database.
- Reason about the security limits of a redirect service (see the
  [threat model](docs/threat-model.md)).

## Features

- `POST /api/links` — create a short link for a valid `http`/`https` URL, with
  an optional custom alias and optional timezone-aware expiry.
- `GET /{code}` — redirect (307) to the destination and increment the click
  count transactionally.
- `GET /api/links/{code}` — read link metadata without redirecting.
- `GET /health` — report local health.
- Duplicate aliases return `409`; missing links `404`; expired links `410`;
  invalid input `422`.
- Interactive OpenAPI docs at `/docs`.

**Non-goals:** no user accounts, billing, distributed analytics, or guaranteed
anti-abuse protection. See the threat model.

## Setup

This project is self-contained with its own dependencies and lockfile. From this
directory:

```sh
cd intermediate/01-url-shortener-api
uv sync                      # install dependencies from uv.lock
uv run alembic upgrade head  # create the database schema
uv run uvicorn --app-dir src url_shortener.main:app --reload
```

The API is then at <http://localhost:8000>, with interactive docs at
<http://localhost:8000/docs>. Configuration is optional; copy
[`.env.example`](.env.example) to `.env` to change defaults.

## Example requests

Create a link with a custom alias:

```sh
curl -X POST http://localhost:8000/api/links \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/some/very/long/path", "alias": "mylink"}'
```

```json
{
  "code": "mylink",
  "short_url": "http://localhost:8000/mylink",
  "url": "https://example.com/some/very/long/path",
  "clicks": 0,
  "created_at": "2026-07-20T08:58:29.919390Z",
  "expires_at": null
}
```

Follow the short link (note the `307` and `Location` header):

```sh
curl -i http://localhost:8000/mylink
# HTTP/1.1 307 Temporary Redirect
# location: https://example.com/some/very/long/path
```

## Tests and quality

From this directory:

```sh
uv run pytest --cov --cov-branch
uv run ruff check .
uv run mypy .
```

Tests use isolated temporary SQLite databases and never require a running server
or real network.

## Architecture

```text
src/url_shortener/
  main.py            # application factory and error handlers
  settings.py        # environment configuration
  api/               # routes and request/response schemas
  application/       # business logic (service, code generation)
  domain/            # domain error types
  infrastructure/    # engine, ORM models, repository
alembic/             # database migrations
```

Layers depend inward: `api` calls `application`, which uses `infrastructure`
through a small repository. Framework and I/O concerns never leak into the
business logic.

## Key decisions

- **Layered, but not over-layered.** Each layer earns its place; there are no
  pass-through-only classes.
- **Migrations, not `create_all`.** The schema is owned by Alembic, matching how
  real services evolve their databases.
- **Atomic click counting.** Redirects increment the counter with a single SQL
  `UPDATE ... SET clicks = clicks + 1`, avoiding read-modify-write races.
- **Strong codes.** Generated codes use `secrets`, so they are not sequential or
  guessable.

## Security and limitations

This is an intentional **open redirector** for learning. It validates URL
*format* but does not vouch for destination *safety*, and it does not fetch
destinations. It has **no rate limiting or authentication**. Click counts are
approximate. Read the [threat model](docs/threat-model.md) before deploying, and
run behind a trusted reverse proxy with TLS and rate limiting.

Reserved aliases (`docs`, `redoc`, `health`) are rejected because they collide
with the API's own routes.

## Container (optional)

A minimal [`Dockerfile`](Dockerfile) is included. It installs runtime
dependencies, runs as a non-root user, applies migrations, and serves the app:

```sh
docker build -t url-shortener-api .
docker run --rm -p 8000:8000 url-shortener-api
```

## Extension challenges

1. Add rate limiting (e.g. per client IP) at the application or proxy layer.
2. Add API-key authentication so only authorised clients can create links.
3. Add pagination and a `GET /api/links` listing endpoint.
4. Move click counting to an append-only events table for real analytics.

## Troubleshooting

- **`no such table: links`** — run `uv run alembic upgrade head` first.
- **`No module named url_shortener`** — start uvicorn with `--app-dir src`.
- **`422` on create** — the URL must be `http`/`https`, the alias must match
  `^[A-Za-z0-9_-]{3,32}$` and not be reserved, and any expiry must be
  timezone-aware and in the future.

## License and contributing

Released under the repository [MIT License](../../LICENSE). See
[CONTRIBUTING.md](../../CONTRIBUTING.md).
