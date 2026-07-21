"""Errors for the password generator."""

from __future__ import annotations


class PolicyError(Exception):
    """Raised when a password policy is impossible or out of bounds."""
