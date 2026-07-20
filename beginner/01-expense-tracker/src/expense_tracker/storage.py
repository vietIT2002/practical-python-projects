"""Safe, atomic JSON persistence for expenses.

The data file is a JSON array of expense objects. JSON is used because it
preserves structure and lets the amount be stored as an exact string; the
tradeoff versus CSV is discussed in the project README.
"""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .errors import StorageError
from .models import Expense


def load_expenses(path: Path) -> list[Expense]:
    """Load expenses from ``path``.

    A missing file is treated as an empty list (first run). A file that exists
    but is malformed raises :class:`StorageError` rather than losing data.
    """
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StorageError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(raw, list):
        raise StorageError(f"{path} must contain a list of expenses")
    return [Expense.from_dict(item) for item in raw]


def save_expenses(path: Path, expenses: list[Expense]) -> None:
    """Write expenses to ``path`` atomically.

    The data is written to a temporary file in the same directory and then moved
    into place with :func:`os.replace`, so an interrupted or failed write never
    corrupts or truncates the existing file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps([expense.to_dict() for expense in expenses], indent=2)

    file_descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(file_descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.write("\n")
        temporary_path.replace(path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise
