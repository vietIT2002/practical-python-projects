# Release process

How to cut a release. Releases use [Semantic Versioning](https://semver.org/).
Publishing steps that touch GitHub are maintainer actions and are only performed
with explicit intent.

## Before tagging

1. Ensure `main` is green in CI on the exact commit to be released.
2. Update [`CHANGELOG.md`](../../CHANGELOG.md): move items from _Unreleased_ into
   the new version section with today's date.
3. Write or update the release notes in `docs/releases/<version>.md`.
4. Run the full local verification:

   ```sh
   uv sync --group dev
   uv run ruff format --check .
   uv run ruff check .
   uv run mypy .
   uv run pytest --cov --cov-branch --cov-report=term-missing --cov-fail-under=85
   uv run python scripts/check_repository.py
   uv run python scripts/validate_project_metadata.py
   uv run python scripts/check_internal_links.py
   uv run python scripts/generate_project_index.py --check
   uv run pip-audit
   ```

5. Verify each self-contained project in its own directory (for example the URL
   Shortener API): `uv sync --group dev`, then ruff, mypy, `alembic upgrade
   head`, and `pytest`, plus `uv run --with pip-audit pip-audit`.

## Tagging and publishing (maintainer action)

Create an annotated tag on the reviewed commit and push it, then create the
GitHub release from that tag:

```sh
git tag -a v0.1.0 -m "Practical Python Projects v0.1.0"
git push origin v0.1.0
```

Create the release on GitHub with the title `v0.1.0`, using the notes from
`docs/releases/v0.1.0.md`. GitHub generates the source archives; do not upload
hand-built artifacts.

## Post-release verification

- [ ] The release page shows the correct tag, title, and notes.
- [ ] The CHANGELOG version links (compare/tag) resolve.
- [ ] The CI badge on the README is green for the tagged commit.
- [ ] Every link in the release notes resolves.
- [ ] Downloading the source archive and following the quick start works from a
      clean extraction (no dependence on local files).
- [ ] The archive contains no secrets, caches, virtual environments, or local
      databases.
- [ ] `git status` is clean and the tag points at the reviewed commit.
