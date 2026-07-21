# Intermediate projects

Projects for people who can write basic Python and are ready to combine several
responsibilities into one well-structured application.

## What "intermediate" means here

- Has more than one responsibility (for example parsing, storage, and a user
  interface).
- May use a small number of well-chosen third-party dependencies.
- Introduces persistence, configuration, or multiple interfaces.
- Expects tests for happy paths, invalid input, and boundary cases.

**You should be comfortable with:** writing functions and classes, using
packages, reading tracebacks, and running tests.

## Projects

<!-- project-index:start -->
| Project | What you build |
|---|---|
| [URL Shortener API](01-url-shortener-api/README.md) | A FastAPI URL shortener with SQLAlchemy, migrations, and isolated tests. |
| [Weather CLI](02-weather-cli/README.md) | A command-line weather client (Open-Meteo, no API key) with unit options, caching, and mocked tests. |
<!-- project-index:end -->

More projects are added incrementally. See the [roadmap](../docs/roadmap.md) for
what is planned, and the [learning paths](../docs/learning-paths.md) for a
suggested order.

## How this level is organised

Each project lives in its own folder named `NN-project-slug` and is
self-contained, with its own dependencies and lockfile when it uses third-party
packages. See the [repository map](../docs/repository-map.md) for naming rules
and project status definitions.
