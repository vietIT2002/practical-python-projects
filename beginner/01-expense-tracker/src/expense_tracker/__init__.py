"""Expense Tracker — a small, dependency-free command-line expense tracker.

The package is organised to keep concerns separate:

- ``models``   — the typed :class:`~expense_tracker.models.Expense` record.
- ``errors``   — the exception hierarchy used across the package.
- ``services`` — pure business logic (create, filter, summarise, delete).
- ``storage``  — safe, atomic JSON persistence.
- ``cli``      — argument parsing and input/output only.
"""

from __future__ import annotations

__version__ = "0.1.0"
