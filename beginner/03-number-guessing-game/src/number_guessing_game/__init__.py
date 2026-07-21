"""A small number guessing game that teaches control flow and testable design.

The game logic is separated from input/output so it can be tested
deterministically by injecting the random source and the read/write functions —
no hidden production backdoor.

Modules:

- ``config`` — difficulty definitions.
- ``game``   — the pure game state machine.
- ``cli``    — argument parsing and the interactive loop.
"""

from __future__ import annotations

__version__ = "0.1.0"
