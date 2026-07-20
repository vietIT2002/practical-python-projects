"""Short-code generation.

Codes use :mod:`secrets` (a cryptographically strong source) rather than
:mod:`random`, so codes are not predictable from one another.
"""

from __future__ import annotations

import secrets
import string

# Base62 alphabet: digits and letters, no ambiguous separators.
ALPHABET = string.ascii_letters + string.digits


def generate_code(length: int) -> str:
    """Return a random base62 code of the given length."""
    return "".join(secrets.choice(ALPHABET) for _ in range(length))
