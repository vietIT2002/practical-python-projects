"""Tests for the Expense model and its (de)serialisation."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from expense_tracker.errors import StorageError
from expense_tracker.models import Expense


def test_to_dict_and_from_dict_round_trip() -> None:
    expense = Expense(
        id="abc123",
        amount=Decimal("12.50"),
        category="food",
        date=date(2026, 7, 20),
        note="lunch",
    )
    assert Expense.from_dict(expense.to_dict()) == expense


def test_to_dict_omits_absent_note() -> None:
    expense = Expense("id1", Decimal("1.00"), "misc", date(2026, 1, 1))
    assert "note" not in expense.to_dict()


def test_from_dict_rejects_non_object() -> None:
    with pytest.raises(StorageError, match="expected an expense object"):
        Expense.from_dict(["not", "a", "dict"])


def test_from_dict_rejects_missing_field() -> None:
    with pytest.raises(StorageError, match="missing field"):
        Expense.from_dict({"id": "x", "amount": "1.00", "category": "food"})


def test_from_dict_rejects_invalid_amount() -> None:
    with pytest.raises(StorageError, match="invalid value"):
        Expense.from_dict(
            {"id": "x", "amount": "abc", "category": "food", "date": "2026-01-01"}
        )


def test_from_dict_rejects_invalid_date() -> None:
    with pytest.raises(StorageError, match="invalid value"):
        Expense.from_dict(
            {"id": "x", "amount": "1.00", "category": "food", "date": "not-a-date"}
        )
