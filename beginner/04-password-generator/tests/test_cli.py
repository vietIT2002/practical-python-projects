"""End-to-end CLI tests."""

from __future__ import annotations

import string

import pytest

from password_generator.cli import main


def test_generates_requested_count(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["--count", "3", "--length", "12"]) == 0
    lines = capsys.readouterr().out.strip().splitlines()
    assert len(lines) == 3
    assert all(len(line) == 12 for line in lines)


def test_digits_only_via_flags(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(["--no-lowercase", "--no-uppercase", "--length", "8"])
    assert exit_code == 0
    password = capsys.readouterr().out.strip()
    assert all(c in string.digits for c in password)


def test_invalid_policy_returns_error(capsys: pytest.CaptureFixture[str]) -> None:
    exit_code = main(
        ["--no-lowercase", "--no-uppercase", "--no-digits"]  # no groups left
    )
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "error" in captured.err
    assert captured.out == ""  # no password printed on failure
