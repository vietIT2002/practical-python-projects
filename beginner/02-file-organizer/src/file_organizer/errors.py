"""Exception hierarchy for the file organizer."""

from __future__ import annotations


class OrganizerError(Exception):
    """Base class for all expected, user-facing errors."""


class ConfigError(OrganizerError):
    """Raised when the category configuration is invalid."""


class PlanError(OrganizerError):
    """Raised when a plan cannot be built (e.g. bad source or destination)."""


class ManifestError(OrganizerError):
    """Raised when a manifest file cannot be read or is malformed."""
