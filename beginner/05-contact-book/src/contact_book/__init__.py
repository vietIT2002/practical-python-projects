"""A contact book CLI that teaches CRUD, search, and safe persistence.

Modules:

- ``errors``     — the exception hierarchy.
- ``models``     — the typed :class:`Contact` record.
- ``validation`` — field validation (basic, documented as not universal).
- ``storage``    — atomic JSON persistence.
- ``service``    — CRUD and search logic.
- ``export``     — CSV export.
- ``cli``        — command-line interface.
"""

from __future__ import annotations

__version__ = "0.1.0"
