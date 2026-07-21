# Number Guessing Game

Guess the secret number in as few attempts as possible. A small game that shows
how to keep logic testable by separating it from input/output and injecting the
random source — no global state, no hidden test backdoor.

- **Difficulty:** beginner
- **Estimated time:** ~2 hours
- **Prerequisites:** functions
- **Python:** 3.12+ (standard library only)

## What you will learn

- Model a small state machine with clear, typed methods.
- Validate user input and give helpful feedback.
- Inject the random source so the game is deterministic under test.
- Support replay with a loop rather than recursion.
- Separate game logic from the command-line interface.

## Features

- Difficulty levels — `easy` (1–10, 5 tries), `medium` (1–50, 8 tries),
  `hard` (1–100, 10 tries).
- Higher/lower feedback and a clear win/lose summary.
- `--seed` for a reproducible game; replay prompt after each round.

**Non-goals:** no graphics, no networking, no persistence.

## Demo

```text
$ python -m number_guessing_game --difficulty easy
Guess a number between 1 and 10. You have 5 attempts.
Your guess: 5
Too low.
Your guess: 8
Too high.
Your guess: 7
Correct!
You won in 3 attempt(s)!
Play again? [y/N]: n
```

## Setup

Standard library only — any Python 3.12+ works. From this directory:

```sh
cd beginner/03-number-guessing-game
PYTHONPATH=src python -m number_guessing_game --help      # Linux/macOS
```

```powershell
$env:PYTHONPATH = "src"; python -m number_guessing_game --help   # Windows
```

## Usage

```text
python -m number_guessing_game [--difficulty {easy,medium,hard}]
                               [--seed N] [--no-replay]
```

## Tests and quality

From the repository root:

```sh
uv run pytest beginner/03-number-guessing-game/tests
uv run ruff check .
uv run mypy .
```

## Architecture

```text
src/number_guessing_game/
  __main__.py   # python -m number_guessing_game
  cli.py        # argument parsing and the interactive loop (I/O injected)
  game.py       # the pure game state machine
  config.py     # difficulty definitions
```

The `Game` class holds no I/O and no global random state, so tests drive it with
a seeded `random.Random` and scripted input/output functions.

## Key decisions

- **Injected randomness.** `new_game(difficulty, rng)` draws the secret from a
  passed-in `random.Random`; tests seed it for determinism. The real CLI uses
  `random.SystemRandom()`.
- **Testable I/O.** `play_round` takes `read_line` and `write_line` callables, so
  the loop is tested without real stdin — this is dependency injection, not a
  production backdoor.

## Limitations

- Single player, single machine; no saved statistics between runs.

## Extension challenges

1. Track and display a best-score across rounds in one session.
2. Add a `--range` option for a custom range and attempt budget.
3. **Toward an intermediate project:** persist results to a file and add a
   summary command — a natural step toward a small stats-tracking CLI or API.

## Troubleshooting

- **`No module named number_guessing_game`** — set `PYTHONPATH=src`, or run from
  the repository root with `uv run`.

## License and contributing

Released under the repository [MIT License](../../LICENSE). See
[CONTRIBUTING.md](../../CONTRIBUTING.md).
