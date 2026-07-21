# Project plan: Secure Password Generator

A milestone path focused on doing randomness and policy correctly.

## Problem

People need strong, unique passwords. A generator must use secure randomness and
honour a character-group policy without weakening it.

## Milestone 1 — the policy

- Model the policy (length and character groups) as typed data.
- Validate it: at least one group, length within bounds; reject the impossible.

## Milestone 2 — secure generation

- Use `secrets` to draw characters.
- Guarantee each selected group appears by drawing one from each first, then
  filling from the pool, then shuffling securely (Fisher–Yates with
  `secrets.randbelow`).
- Test guaranteed properties: length, group membership, and character set.

## Milestone 3 — the interface

- Add CLI options for length, count, and group toggles.
- Print to stdout only; never log a password.
- Return a clear error and exit non-zero on an impossible policy.

## Milestone 4 — polish

- Write the README, including the honest security note about protecting a
  password after generation.
- Ensure formatting, linting, type checking, tests, and metadata pass.

## Definition of Done

Meets the
[Project Definition of Done](../../docs/repository-map.md#draft-vs-published).
