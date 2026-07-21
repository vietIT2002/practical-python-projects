"""Command-line interface: argument parsing and the interactive loop.

Input and output are injected so the loop can be tested without real stdin.
"""

from __future__ import annotations

import argparse
import random
from collections.abc import Callable

from . import __version__
from .config import DEFAULT_DIFFICULTY, DIFFICULTIES
from .game import Game, GuessOutcome, difficulty_by_name, new_game

ReadLine = Callable[[str], str]
WriteLine = Callable[[str], None]

_FEEDBACK = {
    GuessOutcome.TOO_LOW: "Too low.",
    GuessOutcome.TOO_HIGH: "Too high.",
    GuessOutcome.CORRECT: "Correct!",
}


def play_round(game: Game, read_line: ReadLine, write_line: WriteLine) -> None:
    """Play a single round to completion using injected I/O."""
    write_line(
        f"Guess a number between {game.low} and {game.high}. "
        f"You have {game.max_attempts} attempts."
    )
    while not game.is_over:
        raw = read_line("Your guess: ").strip()
        try:
            value = int(raw)
        except ValueError:
            write_line("Please enter a whole number.")
            continue
        try:
            outcome = game.guess(value)
        except ValueError as error:
            write_line(str(error))
            continue
        write_line(_FEEDBACK[outcome])

    if game.has_won:
        write_line(f"You won in {game.attempts_made} attempt(s)!")
    else:
        write_line(f"Out of attempts. The number was {game.secret}.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="number-guessing-game", description="Guess the secret number."
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--difficulty",
        choices=sorted(DIFFICULTIES),
        default=DEFAULT_DIFFICULTY,
        help=f"difficulty level (default: {DEFAULT_DIFFICULTY})",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="seed the random source for a reproducible game",
    )
    parser.add_argument(
        "--no-replay",
        action="store_true",
        help="play a single round and exit (no replay prompt)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    difficulty = difficulty_by_name(args.difficulty)
    rng = random.Random(args.seed) if args.seed is not None else random.SystemRandom()

    def read_line(prompt: str) -> str:
        return input(prompt)

    def write_line(message: str) -> None:
        print(message)

    while True:
        play_round(new_game(difficulty, rng), read_line, write_line)
        if args.no_replay:
            return 0
        answer = read_line("Play again? [y/N]: ").strip().lower()
        if answer not in {"y", "yes"}:
            return 0


if __name__ == "__main__":
    raise SystemExit(main())
