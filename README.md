# Practical Python Projects

Learn Python by building practical, tested, and production-minded projects.

> **Status: early foundation.** The repository structure and toolchain are in
> place; learning projects are being added incrementally. See the
> [roadmap](docs/roadmap.md) for what is planned.

## Who this is for

Self-taught learners, students, and developers who want to learn Python by
completing real, well-structured projects — each one runnable from documented
commands and backed by tests.

## Browse projects by level

- [Beginner](beginner/README.md) — small, standard-library projects.
- [Intermediate](intermediate/README.md) — structured applications.
- [Advanced](advanced/README.md) — services, pipelines, and integrations.

New here? Follow a [learning path](docs/learning-paths.md) instead of picking at
random.

## Quick start

You need [Python 3.12+](https://www.python.org/downloads/),
[uv](https://docs.astral.sh/uv/), and git. From the repository root:

```sh
uv sync --group dev        # install the development toolchain
uv run pytest              # run the tests
```

Full setup and the complete list of quality commands are in the
[development environment guide](docs/getting-started/development-environment.md).

## Quality

Every published project is expected to be runnable from a clean clone, tested at
happy-path, invalid-input, and boundary levels, and to pass formatting, linting,
type checking, and tests. See [draft vs published](docs/repository-map.md#draft-vs-published)
for the exact bar.

## Documentation

- [Documentation home](docs/README.md)
- [Repository map](docs/repository-map.md) — where everything lives.
- [Architecture decisions](docs/architecture/README.md) — why it is built this
  way.

## Contributing

A full contribution guide is being prepared. Until then, please open an issue to
discuss ideas or report problems.

## License

Released under the [MIT License](LICENSE).
