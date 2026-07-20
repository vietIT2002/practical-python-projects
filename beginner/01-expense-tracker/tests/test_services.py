"""Tests for the pure business logic."""

from __future__ import annotations

from datetime import date
from decimal import Decimal

import pytest

from expense_tracker.errors import ExpenseNotFoundError, ValidationError
from expense_tracker.models import Expense
from expense_tracker.services import (
    create_expense,
    delete_expense,
    filter_expenses,
    summarise,
)


def _fixed_id() -> str:
    return "fixed001"


def test_create_expense_valid() -> None:
    expense = create_expense(
        amount="12.5", category=" food ", on_date="2026-07-20", id_factory=_fixed_id
    )
    assert expense.id == "fixed001"
    assert expense.amount == Decimal("12.50")  # quantised to cents
    assert expense.category == "food"  # trimmed
    assert expense.date == date(2026, 7, 20)


def test_create_expense_rounds_to_cents() -> None:
    expense = create_expense(
        amount="12.999", category="x", on_date="2026-07-20", id_factory=_fixed_id
    )
    assert expense.amount == Decimal("13.00")


def test_blank_note_becomes_none() -> None:
    expense = create_expense(
        amount="1", category="x", on_date="2026-07-20", note="   ", id_factory=_fixed_id
    )
    assert expense.note is None


@pytest.mark.parametrize("amount", ["abc", "0", "-5", "NaN", "Infinity"])
def test_invalid_amount_rejected(amount: str) -> None:
    with pytest.raises(ValidationError):
        create_expense(amount=amount, category="x", on_date="2026-07-20")


def test_empty_category_rejected() -> None:
    with pytest.raises(ValidationError, match="category"):
        create_expense(amount="1", category="   ", on_date="2026-07-20")


def test_invalid_date_rejected() -> None:
    with pytest.raises(ValidationError, match="date"):
        create_expense(amount="1", category="x", on_date="20-07-2026")


def test_note_too_long_rejected() -> None:
    with pytest.raises(ValidationError, match="note"):
        create_expense(amount="1", category="x", on_date="2026-07-20", note="a" * 201)


def _sample() -> list[Expense]:
    return [
        Expense("1", Decimal("10.00"), "food", date(2026, 7, 1)),
        Expense("2", Decimal("20.00"), "travel", date(2026, 7, 15)),
        Expense("3", Decimal("5.00"), "Food", date(2026, 8, 2)),
    ]


def test_filter_by_month() -> None:
    result = filter_expenses(_sample(), month="2026-07")
    assert {e.id for e in result} == {"1", "2"}


def test_filter_by_category_is_case_insensitive() -> None:
    result = filter_expenses(_sample(), category="food")
    assert {e.id for e in result} == {"1", "3"}


def test_filter_invalid_month_rejected() -> None:
    with pytest.raises(ValidationError, match="month"):
        filter_expenses(_sample(), month="2026-13")


def test_summarise_uses_exact_decimals() -> None:
    expenses = [
        Expense("a", Decimal("0.10"), "x", date(2026, 7, 1)),
        Expense("b", Decimal("0.20"), "x", date(2026, 7, 2)),
    ]
    summary = summarise(expenses)
    assert summary.total == Decimal("0.30")
    assert summary.by_category == {"x": Decimal("0.30")}
    assert summary.by_month == {"2026-07": Decimal("0.30")}


def test_delete_existing() -> None:
    remaining = delete_expense(_sample(), "2")
    assert {e.id for e in remaining} == {"1", "3"}


def test_delete_missing_raises() -> None:
    with pytest.raises(ExpenseNotFoundError, match="nope"):
        delete_expense(_sample(), "nope")
