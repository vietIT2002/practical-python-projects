"""Domain error hierarchy, mapped to HTTP responses in the API layer."""

from __future__ import annotations


class DomainError(Exception):
    """Base class for expected domain errors."""


class LinkNotFoundError(DomainError):
    """Raised when a code has no matching link."""


class LinkExpiredError(DomainError):
    """Raised when a link exists but has expired."""


class AliasConflictError(DomainError):
    """Raised when a requested custom alias is already taken."""


class CodeGenerationError(DomainError):
    """Raised when a unique code could not be generated after several tries."""
