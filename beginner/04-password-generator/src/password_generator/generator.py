"""Password generation using cryptographically secure randomness."""

from __future__ import annotations

import secrets

from .errors import PolicyError
from .policy import Policy


def _secure_shuffle(items: list[str]) -> None:
    """Shuffle in place with a Fisher-Yates using a secure random source."""
    for index in range(len(items) - 1, 0, -1):
        swap = secrets.randbelow(index + 1)
        items[index], items[swap] = items[swap], items[index]


def generate_password(policy: Policy) -> str:
    """Generate one password satisfying the policy.

    Each selected character group is guaranteed to appear at least once: one
    character is drawn from every group first, the rest are drawn from the
    combined pool, and the result is shuffled securely. This avoids biased or
    fragile "generate and retry until it matches" loops.
    """
    groups = policy.validate()
    pool = "".join(groups)

    characters = [secrets.choice(group) for group in groups]
    characters += [secrets.choice(pool) for _ in range(policy.length - len(characters))]
    _secure_shuffle(characters)
    return "".join(characters)


def generate_passwords(policy: Policy, count: int) -> list[str]:
    """Generate ``count`` passwords for the policy."""
    if count < 1:
        raise PolicyError("count must be at least 1")
    return [generate_password(policy) for _ in range(count)]
