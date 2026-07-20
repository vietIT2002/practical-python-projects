"""Exception hierarchy for the expense tracker.

Using specific exceptions lets the CLI translate domain problems into clear
messages and exit codes without leaking stack traces to users.
"""

from __future__ import annotations


class ExpenseError(Exception):
    """Base class for all expected, user-facing errors."""


class ValidationError(ExpenseError):
    """Raised when user-provided data is invalid."""


class ExpenseNotFoundError(ExpenseError):
    """Raised when an expense id does not exist."""


class StorageError(ExpenseError):
    """Raised when the data file cannot be read or is malformed."""
