"""Entry point so the package runs with ``python -m website_change_monitor``."""

from __future__ import annotations

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
