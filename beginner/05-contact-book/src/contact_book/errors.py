"""Exception hierarchy for the contact book."""

from __future__ import annotations


class ContactError(Exception):
    """Base class for expected, user-facing errors."""


class ValidationError(ContactError):
    """Raised when contact fields are invalid."""


class ContactNotFoundError(ContactError):
    """Raised when a contact id does not exist."""


class StorageError(ContactError):
    """Raised when the data file cannot be read or is malformed."""


class ExportError(ContactError):
    """Raised when an export target is invalid or would be overwritten."""
