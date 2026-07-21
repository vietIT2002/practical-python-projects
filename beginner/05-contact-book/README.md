# Contact Book CLI

Manage a local contact book from the command line: add, list, search, update,
delete, and export contacts. A small but complete CRUD application with safe
storage.

- **Difficulty:** beginner
- **Estimated time:** ~3 hours
- **Prerequisites:** functions, basic classes
- **Python:** 3.12+ (standard library only)

## What you will learn

- Implement CRUD operations over a typed data model.
- Search with case-insensitive normalization.
- Persist data as JSON, written atomically.
- Export to CSV without overwriting files by accident.
- Validate input honestly (and know the limits of that validation).

## Features

- `add`, `list`, `search`, `update`, and `delete` contacts.
- Stable ids; update changes only the fields you pass.
- Optional email and phone with basic validation.
- Configurable `--data-file`; atomic JSON persistence.
- `export` to a CSV path, refusing to overwrite unless `--force`.

**Non-goals:** no encryption, no cloud sync, no deduplication.

## Demo

```text
$ python -m contact_book --data-file contacts.json add --name "Ada Lovelace" --email ada@example.com
Added contact 4f9a2b1c: Ada Lovelace

$ python -m contact_book --data-file contacts.json list
ID          NAME                      EMAIL                         PHONE
4f9a2b1c    Ada Lovelace              ada@example.com               -

$ python -m contact_book --data-file contacts.json search lovelace
ID          NAME                      EMAIL                         PHONE
4f9a2b1c    Ada Lovelace              ada@example.com               -
```

## Setup

Standard library only — any Python 3.12+ works. From this directory:

```sh
cd beginner/05-contact-book
PYTHONPATH=src python -m contact_book --help      # Linux/macOS
```

```powershell
$env:PYTHONPATH = "src"; python -m contact_book --help   # Windows
```

## Usage

```text
python -m contact_book [--data-file PATH] <command> ...

  add     --name NAME [--email EMAIL] [--phone PHONE]
  list
  search  QUERY
  update  ID [--name ...] [--email ...] [--phone ...]
  delete  ID
  export  PATH [--force]
```

## Tests and quality

From the repository root:

```sh
uv run pytest beginner/05-contact-book/tests
uv run ruff check .
uv run mypy .
```

## Architecture

```text
src/contact_book/
  __main__.py    # python -m contact_book
  cli.py         # argument parsing and input/output
  service.py     # CRUD and search (pure functions)
  validation.py  # basic field validation
  storage.py     # atomic JSON persistence
  export.py      # CSV export
  models.py      # the typed Contact record
  errors.py      # the exception hierarchy
```

## Key decisions

- **Atomic writes.** Saving writes to a temporary file and replaces the target,
  so an interrupted save never corrupts the contact list.
- **Export never clobbers.** CSV export refuses to overwrite an existing file
  unless `--force` is given.
- **Honest validation.** Email and phone checks catch common mistakes but are
  intentionally simple — they are not universal validators.

## Security and privacy

Contacts are stored in a plain, **unencrypted** local JSON file. Do not use this
for sensitive contacts without adding your own protection (for example full-disk
encryption or an encrypted container). The sample data in tests is synthetic.

## Limitations

- Single user, single file; no concurrent-write coordination.
- Validation is basic by design and does not guarantee deliverability.

## Extension challenges

1. Add groups or tags and filter the list by them.
2. Add an `import` command that reads the exported CSV back in.
3. **Toward an intermediate project:** put the contacts behind a small HTTP API
   with a database — a natural bridge to the URL Shortener API's patterns.

## Troubleshooting

- **`No module named contact_book`** — set `PYTHONPATH=src`, or run from the
  repository root with `uv run`.
- **`error: ... already exists`** on export — pass `--force` to overwrite.

## License and contributing

Released under the repository [MIT License](../../LICENSE). See
[CONTRIBUTING.md](../../CONTRIBUTING.md).
