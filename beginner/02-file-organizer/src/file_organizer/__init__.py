"""Safe File Organizer — plan, apply, and undo tidy file moves by category.

Safety is the theme of this project:

- A dry run is the default; nothing moves until you pass ``--apply``.
- Existing files are never overwritten.
- Directories and symlinks are ignored.
- Every applied run writes a manifest so the moves can be undone.

Modules:

- ``models``    — the typed :class:`Move`, :class:`Skip`, and :class:`Plan`.
- ``errors``    — the exception hierarchy.
- ``classify``  — extension-to-category rules (with optional config).
- ``planner``   — builds a plan without touching the filesystem.
- ``executor``  — applies and undoes moves, reporting partial failure.
- ``manifest``  — reads and writes the operation manifest.
- ``cli``       — argument parsing and input/output only.
"""

from __future__ import annotations

__version__ = "0.1.0"
