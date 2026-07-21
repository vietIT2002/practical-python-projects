"""Entry point so the package runs with ``python -m weather_cli``."""

from __future__ import annotations

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
