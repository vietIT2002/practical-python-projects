# Project plan: Safe File Organizer CLI

A milestone-by-milestone path a learner can follow. The theme throughout is
safety: plan before you act, never overwrite, and always be able to undo.

## Problem

A cluttered downloads or inbox folder is tedious to sort by hand. A CLI can do
it — but moving files is risky, so the design must make mistakes hard.

## Milestone 1 — classification

- Define default extension-to-category rules.
- Support an optional JSON config, validating category names as safe path
  components.
- Test case-insensitive extensions, unknown extensions, and invalid configs.

## Milestone 2 — planning (pure)

- Scan the source directory (no recursion); skip directories and symlinks.
- Compute each destination and resolve conflicts with a numeric suffix.
- Keep destinations inside the destination root.
- Test that planning changes nothing on disk.

## Milestone 3 — applying

- Move files, creating category folders as needed.
- Never overwrite; stop at the first failure and report completed vs pending.
- Write a manifest of completed moves atomically.
- Test moves, the no-overwrite guard, and partial failure.

## Milestone 4 — undo

- Read the manifest and reverse each move.
- Refuse any reversal that is missing or would overwrite the original.
- Test a full round trip and refusals.

## Milestone 5 — CLI and polish

- Add `organize` and `undo` subcommands with a dry-run default.
- Send output to stdout, errors to stderr, and return correct exit codes.
- Write the README with a prominent backup warning and a temporary-folder demo.
- Ensure formatting, linting, type checking, tests, and metadata all pass.

## Definition of Done

The project is complete when it meets the
[Project Definition of Done](../../docs/repository-map.md#draft-vs-published):
full README, tests at all three levels, passing quality checks, and valid
metadata.
