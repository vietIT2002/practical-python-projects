"""Tests for the CLI loop using scripted input/output (no real stdin)."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from number_guessing_game.cli import main, play_round
from number_guessing_game.game import Game


def _reader(lines: list[str]) -> tuple[object, list[str]]:
    it: Iterator[str] = iter(lines)
    prompts: list[str] = []

    def read_line(prompt: str) -> str:
        prompts.append(prompt)
        return next(it)

    return read_line, prompts


def _collector() -> tuple[object, list[str]]:
    out: list[str] = []

    def write_line(message: str) -> None:
        out.append(message)

    return write_line, out


def test_play_round_win() -> None:
    game = Game(1, 100, 5, secret=42)
    read_line, _ = _reader(["10", "90", "42"])
    write_line, out = _collector()
    play_round(game, read_line, write_line)  # type: ignore[arg-type]
    joined = "\n".join(out)
    assert "Correct!" in joined
    assert "You won in 3 attempt(s)!" in joined


def test_play_round_loss_reveals_secret() -> None:
    game = Game(1, 100, 2, secret=42)
    read_line, _ = _reader(["1", "2"])
    write_line, out = _collector()
    play_round(game, read_line, write_line)  # type: ignore[arg-type]
    assert any("The number was 42" in line for line in out)


def test_play_round_handles_non_integer_and_out_of_range() -> None:
    game = Game(1, 10, 5, secret=5)
    read_line, _ = _reader(["abc", "99", "5"])
    write_line, out = _collector()
    play_round(game, read_line, write_line)  # type: ignore[arg-type]
    joined = "\n".join(out)
    assert "Please enter a whole number." in joined
    assert "between 1 and 10" in joined
    assert "Correct!" in joined


def test_main_single_round_returns_zero(monkeypatch: pytest.MonkeyPatch) -> None:
    answers = iter(["5", "5", "5", "5", "5"])
    monkeypatch.setattr("builtins.input", lambda _prompt="": next(answers))
    exit_code = main(["--difficulty", "easy", "--seed", "1", "--no-replay"])
    assert exit_code == 0
