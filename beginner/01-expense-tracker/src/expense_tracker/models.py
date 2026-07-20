"""The typed expense record and its (de)serialisation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal, InvalidOperation
from typing import Any

from .errors import StorageError

#: Maximum length of an expense note.
NOTE_MAX_LENGTH = 200


@dataclass(frozen=True)
class Expense:
    """A single expense.

    ``amount`` is a :class:`~decimal.Decimal` so money is exact — never a binary
    float. On disk the amount is stored as a string to preserve that exactness.
    """

    id: str
    amount: Decimal
    category: str
    date: date
    note: str | None = None

    def to_dict(self) -> dict[str, str]:
        """Convert to a JSON-serialisable dictionary."""
        record = {
            "id": self.id,
            "amount": str(self.amount),
            "category": self.category,
            "date": self.date.isoformat(),
        }
        if self.note is not None:
            record["note"] = self.note
        return record

    @classmethod
    def from_dict(cls, data: Any) -> Expense:
        """Rebuild an expense from stored data.

        Raises :class:`StorageError` with an actionable message if the stored
        record is malformed, so a corrupt file never silently loses data.
        """
        if not isinstance(data, dict):
            raise StorageError(f"expected an expense object, got {type(data).__name__}")
        try:
            identifier = str(data["id"])
            amount = Decimal(str(data["amount"]))
            category = str(data["category"])
            stored_date = date.fromisoformat(str(data["date"]))
        except KeyError as exc:
            raise StorageError(f"stored expense is missing field {exc}") from exc
        except (InvalidOperation, ValueError) as exc:
            raise StorageError(f"stored expense has an invalid value: {exc}") from exc

        note = data.get("note")
        if note is not None:
            note = str(note)
        return cls(
            id=identifier,
            amount=amount,
            category=category,
            date=stored_date,
            note=note,
        )
