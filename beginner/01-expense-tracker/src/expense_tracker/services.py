"""Business logic for the expense tracker.

These functions are pure: they take and return data and never read arguments,
print output, or touch the filesystem. That keeps them easy to test and reuse.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from uuid import uuid4

from .errors import ExpenseNotFoundError, ValidationError
from .models import NOTE_MAX_LENGTH, Expense

#: A factory that returns a new unique expense id.
IdFactory = Callable[[], str]

_CENTS = Decimal("0.01")


def _default_id() -> str:
    return uuid4().hex[:8]


def create_expense(
    *,
    amount: str,
    category: str,
    on_date: str,
    note: str | None = None,
    id_factory: IdFactory = _default_id,
) -> Expense:
    """Validate raw input and build an :class:`Expense`.

    ``amount`` is parsed as a :class:`~decimal.Decimal`, must be positive, and is
    rounded to two decimal places. ``on_date`` must be ISO ``YYYY-MM-DD``.
    """
    parsed_amount = _parse_amount(amount)
    parsed_category = _parse_category(category)
    parsed_date = _parse_date(on_date)
    parsed_note = _parse_note(note)
    return Expense(
        id=id_factory(),
        amount=parsed_amount,
        category=parsed_category,
        date=parsed_date,
        note=parsed_note,
    )


def _parse_amount(amount: str) -> Decimal:
    try:
        value = Decimal(amount)
    except InvalidOperation:
        raise ValidationError(f"amount {amount!r} is not a valid number") from None
    if not value.is_finite():
        raise ValidationError(f"amount {amount!r} is not a finite number")
    if value <= 0:
        raise ValidationError("amount must be greater than zero")
    return value.quantize(_CENTS)


def _parse_category(category: str) -> str:
    cleaned = category.strip()
    if not cleaned:
        raise ValidationError("category must not be empty")
    return cleaned


def _parse_date(on_date: str) -> date:
    try:
        return date.fromisoformat(on_date)
    except ValueError:
        raise ValidationError(
            f"date {on_date!r} must be in ISO format, e.g. 2026-07-20"
        ) from None


def _parse_note(note: str | None) -> str | None:
    if note is None:
        return None
    cleaned = note.strip()
    if not cleaned:
        return None
    if len(cleaned) > NOTE_MAX_LENGTH:
        raise ValidationError(f"note must be at most {NOTE_MAX_LENGTH} characters")
    return cleaned


def filter_expenses(
    expenses: Iterable[Expense],
    *,
    month: str | None = None,
    category: str | None = None,
) -> list[Expense]:
    """Return expenses matching an optional ``month`` (``YYYY-MM``) and category.

    Category matching is case-insensitive.
    """
    if month is not None:
        _validate_month(month)
    wanted_category = category.strip().lower() if category else None

    result = []
    for expense in expenses:
        if month is not None and expense.date.strftime("%Y-%m") != month:
            continue
        if wanted_category is not None and expense.category.lower() != wanted_category:
            continue
        result.append(expense)
    return result


def _validate_month(month: str) -> None:
    try:
        date.fromisoformat(f"{month}-01")
    except ValueError:
        raise ValidationError(
            f"month {month!r} must be in ISO format, e.g. 2026-07"
        ) from None


@dataclass(frozen=True)
class Summary:
    """Aggregated totals for a set of expenses."""

    total: Decimal
    by_month: dict[str, Decimal]
    by_category: dict[str, Decimal]


def summarise(expenses: Iterable[Expense]) -> Summary:
    """Total the expenses overall, by month, and by category."""
    total = Decimal("0.00")
    by_month: dict[str, Decimal] = {}
    by_category: dict[str, Decimal] = {}
    for expense in expenses:
        total += expense.amount
        month = expense.date.strftime("%Y-%m")
        by_month[month] = by_month.get(month, Decimal("0.00")) + expense.amount
        by_category[expense.category] = (
            by_category.get(expense.category, Decimal("0.00")) + expense.amount
        )
    return Summary(
        total=total,
        by_month=dict(sorted(by_month.items())),
        by_category=dict(sorted(by_category.items())),
    )


def delete_expense(expenses: Iterable[Expense], expense_id: str) -> list[Expense]:
    """Return a new list without the expense whose id matches ``expense_id``.

    Raises :class:`ExpenseNotFoundError` if no expense has that id.
    """
    original = list(expenses)
    remaining = [expense for expense in original if expense.id != expense_id]
    if len(remaining) == len(original):
        raise ExpenseNotFoundError(f"no expense found with id {expense_id!r}")
    return remaining
