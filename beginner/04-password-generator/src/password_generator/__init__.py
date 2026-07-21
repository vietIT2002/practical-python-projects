"""A secure password generator that teaches cryptographic randomness.

Passwords are generated with :mod:`secrets` (never :mod:`random`), and the
selected character-group requirements are guaranteed by construction rather than
by a fragile retry loop.

Modules:

- ``errors``    — the policy error type.
- ``policy``    — the password policy and its validation.
- ``generator`` — password generation.
- ``cli``       — command-line interface.
"""

from __future__ import annotations

__version__ = "0.1.0"
