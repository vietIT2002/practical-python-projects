"""A small URL shortener HTTP API built with FastAPI and SQLAlchemy.

Layered on purpose:

- ``api``            — HTTP contracts, routes, and request/response schemas.
- ``application``    — business logic (creating links, redirecting, counting).
- ``domain``         — the domain error types.
- ``infrastructure`` — database engine, models, and data access.
- ``settings``       — environment-based configuration.
- ``main``           — the application factory.
"""

from __future__ import annotations

__version__ = "0.1.0"
