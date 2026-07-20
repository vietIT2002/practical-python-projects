# Project plan: Expense Tracker CLI

A milestone-by-milestone path a learner can follow to build this project. Each
milestone ends in something runnable or testable.

## Problem

People want a quick way to record and review spending without a spreadsheet or
an account. A small CLI teaches data modelling, money handling, validation, and
safe file storage.

## Milestone 1 — model the data

- Create a frozen `Expense` dataclass: id, amount (`Decimal`), category, date,
  optional note.
- Add `to_dict` / `from_dict`, storing the amount as a string.
- Test a round trip and rejection of malformed stored records.

## Milestone 2 — business logic

- Write pure functions: `create_expense` (with validation), `filter_expenses`,
  `summarise`, and `delete_expense`.
- Validate amount (positive, two decimals), category (non-empty), date (ISO),
  and note length.
- Test valid input, each invalid case, and `0.10 + 0.20 == 0.30`.

## Milestone 3 — storage

- Load returns `[]` when the file is missing; a malformed file raises a clear
  error.
- Save writes to a temporary file and replaces the target atomically.
- Test the round trip and that a failed write preserves the existing file.

## Milestone 4 — command-line interface

- Add `add`, `list`, `summary`, and `delete` subcommands and a `--data-file`
  option.
- Send normal output to stdout, errors to stderr, and return exit code `1` on a
  domain error.
- Test one successful and one failing command end to end.

## Milestone 5 — polish

- Write the README following the project contract.
- Add synthetic sample data.
- Ensure formatting, linting, type checking, tests, and metadata validation all
  pass.

## Definition of Done

The project is complete when it meets the
[Project Definition of Done](../../docs/repository-map.md#draft-vs-published):
full README, tests at all three levels, passing quality checks, and valid
metadata.
