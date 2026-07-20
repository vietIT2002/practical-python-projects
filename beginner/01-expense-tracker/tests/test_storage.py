"""Tests for JSON persistence, including atomic-write safety."""

from __future__ import annotations

import os
from datetime import date
from decimal import Decimal
from pathlib import Path

import pytest

from expense_tracker import storage
from expense_tracker.errors import StorageError
from expense_tracker.models import Expense


def test_load_missing_file_returns_empty(tmp_path: Path) -> None:
    assert storage.load_expenses(tmp_path / "nope.json") == []


def test_save_then_load_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    expenses = [
        Expense("1", Decimal("10.00"), "food", date(2026, 7, 1), "lunch"),
        Expense("2", Decimal("20.00"), "travel", date(2026, 7, 2)),
    ]
    storage.save_expenses(path, expenses)
    assert storage.load_expenses(path) == expenses


def test_save_creates_missing_parent_directory(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "dir" / "data.json"
    storage.save_expenses(path, [])
    assert path.is_file()


def test_load_invalid_json_raises(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    path.write_text("{ not json", encoding="utf-8")
    with pytest.raises(StorageError, match="not valid JSON"):
        storage.load_expenses(path)


def test_load_non_list_raises(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    path.write_text('{"id": "1"}', encoding="utf-8")
    with pytest.raises(StorageError, match="must contain a list"):
        storage.load_expenses(path)


def test_load_malformed_item_raises(tmp_path: Path) -> None:
    path = tmp_path / "data.json"
    path.write_text('[{"id": "1"}]', encoding="utf-8")
    with pytest.raises(StorageError):
        storage.load_expenses(path)


def test_failed_write_preserves_existing_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "data.json"
    original = [Expense("1", Decimal("10.00"), "food", date(2026, 7, 1))]
    storage.save_expenses(path, original)
    before = path.read_text(encoding="utf-8")

    def boom(src: object, dst: object) -> None:
        raise OSError("simulated failure")

    monkeypatch.setattr(os, "replace", boom)

    new_expense = [Expense("2", Decimal("99.00"), "x", date(2026, 7, 2))]
    with pytest.raises(OSError, match="simulated failure"):
        storage.save_expenses(path, new_expense)

    # The original data is intact and no temporary file was left behind.
    assert path.read_text(encoding="utf-8") == before
    leftover = list(tmp_path.glob("*.tmp"))
    assert leftover == []
