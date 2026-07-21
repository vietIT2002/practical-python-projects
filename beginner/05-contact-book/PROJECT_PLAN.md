# Project plan: Contact Book CLI

A milestone path for a small but complete CRUD application.

## Problem

A simple, local contact book: add, find, update, delete contacts, and export
them — with safe storage and honest validation.

## Milestone 1 — model and validation

- Define a typed `Contact` with optional email and phone.
- Add basic, clearly-not-universal validation for name, email, and phone.

## Milestone 2 — storage

- Load returns `[]` for a missing file; malformed data errors clearly.
- Save writes atomically (temp file + replace).

## Milestone 3 — CRUD and search

- Implement create, find (case-insensitive substring), get, update, delete.
- Use stable identifiers; update only the fields provided.

## Milestone 4 — export

- Export to CSV at an explicit path; refuse to overwrite without `--force`.

## Milestone 5 — interface and polish

- Add CLI subcommands and a configurable data-file path.
- Write the README, including the storage-is-not-encrypted note.
- Ensure formatting, linting, type checking, tests, and metadata pass.

## Definition of Done

Meets the
[Project Definition of Done](../../docs/repository-map.md#draft-vs-published).
