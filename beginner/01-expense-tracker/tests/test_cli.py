"""End-to-end tests for the command-line interface."""

from __future__ import annotations

from pathlib import Path

import pytest

from expense_tracker.cli import main


def _data_file(tmp_path: Path) -> list[str]:
    return ["--data-file", str(tmp_path / "expenses.json")]


def test_add_then_list_round_trip(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    base = _data_file(tmp_path)
    assert (
        main(
            [
                *base,
                "add",
                "--amount",
                "12.50",
                "--category",
                "food",
                "--date",
                "2026-07-20",
            ]
        )
        == 0
    )
    assert "Added expense" in capsys.readouterr().out

    assert main([*base, "list"]) == 0
    out = capsys.readouterr().out
    assert "food" in out
    assert "12.50" in out


def test_list_empty_reports_no_expenses(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert main([*_data_file(tmp_path), "list"]) == 0
    assert "No expenses found." in capsys.readouterr().out


def test_add_invalid_amount_returns_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    exit_code = main(
        [*_data_file(tmp_path), "add", "--amount", "-5", "--category", "food"]
    )
    assert exit_code == 1
    assert "error" in capsys.readouterr().err


def test_summary_reports_totals(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    base = _data_file(tmp_path)
    main([*base, "add", "--amount", "0.10", "--category", "x", "--date", "2026-07-01"])
    main([*base, "add", "--amount", "0.20", "--category", "x", "--date", "2026-07-02"])
    capsys.readouterr()
    assert main([*base, "summary"]) == 0
    out = capsys.readouterr().out
    assert "Total: 0.30" in out


def test_delete_existing_and_missing(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    base = _data_file(tmp_path)
    main([*base, "add", "--amount", "5", "--category", "food", "--date", "2026-07-01"])
    added = capsys.readouterr().out
    expense_id = added.split("Added expense ")[1].split(":")[0].strip()

    assert main([*base, "delete", expense_id]) == 0
    assert "Deleted expense" in capsys.readouterr().out

    assert main([*base, "delete", "missing-id"]) == 1
    assert "error" in capsys.readouterr().err


def test_list_filters_by_month(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    base = _data_file(tmp_path)
    main([*base, "add", "--amount", "10", "--category", "food", "--date", "2026-07-01"])
    main([*base, "add", "--amount", "20", "--category", "food", "--date", "2026-08-01"])
    capsys.readouterr()
    assert main([*base, "list", "--month", "2026-08"]) == 0
    out = capsys.readouterr().out
    assert "20.00" in out
    assert "10.00" not in out
