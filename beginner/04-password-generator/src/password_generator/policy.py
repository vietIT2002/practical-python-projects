"""The password policy: which character groups to use and how long."""

from __future__ import annotations

import string
from dataclasses import dataclass

from .errors import PolicyError

# A conservative symbol set: punctuation that is safe to paste and unlikely to
# break shells or CSV. Quotes, backslash, spaces, and backticks are excluded.
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.?"

LOWERCASE = string.ascii_lowercase
UPPERCASE = string.ascii_uppercase
DIGITS = string.digits

# The minimum length is at least the number of character groups (4), so a valid
# length always has room for one character from every selected group.
MIN_LENGTH = 4
MAX_LENGTH = 256


@dataclass(frozen=True)
class Policy:
    """Which character groups to include and the desired length."""

    length: int = 16
    use_lowercase: bool = True
    use_uppercase: bool = True
    use_digits: bool = True
    use_symbols: bool = False

    def selected_groups(self) -> list[str]:
        groups: list[str] = []
        if self.use_lowercase:
            groups.append(LOWERCASE)
        if self.use_uppercase:
            groups.append(UPPERCASE)
        if self.use_digits:
            groups.append(DIGITS)
        if self.use_symbols:
            groups.append(SYMBOLS)
        return groups

    def validate(self) -> list[str]:
        """Return the selected groups, or raise :class:`PolicyError`."""
        groups = self.selected_groups()
        if not groups:
            raise PolicyError("select at least one character group")
        if not MIN_LENGTH <= self.length <= MAX_LENGTH:
            raise PolicyError(f"length must be between {MIN_LENGTH} and {MAX_LENGTH}")
        return groups
