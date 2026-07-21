# Project plan: Number Guessing Game

A milestone path for building the game with clean, testable structure.

## Problem

A classic first game — but built properly: deterministic under test and with
logic separated from input/output.

## Milestone 1 — difficulty config

- Define difficulty levels (range and attempt budget) as typed data.

## Milestone 2 — the game state machine

- Implement `Game` with `guess`, attempt tracking, and win/over state.
- Reject out-of-range guesses and guesses after the game ends.
- Draw the secret from an injected `random.Random`.
- Test outcomes deterministically with a seeded source.

## Milestone 3 — the interface

- Add a CLI with difficulty, `--seed`, and `--no-replay` options.
- Loop for guesses and replay (no recursion); inject `read_line`/`write_line`.
- Test the loop with scripted input and collected output.

## Milestone 4 — polish

- Write the README with a demo and clear setup.
- Ensure formatting, linting, type checking, tests, and metadata pass.

## Definition of Done

Meets the
[Project Definition of Done](../../docs/repository-map.md#draft-vs-published).
