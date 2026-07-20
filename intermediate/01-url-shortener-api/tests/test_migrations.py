"""Verify the Alembic migration builds the schema from an empty database."""

from __future__ import annotations

from pathlib import Path

from alembic.config import Config
from sqlalchemy import create_engine, inspect

from alembic import command

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_migration_from_empty_database(tmp_path: Path) -> None:
    database = tmp_path / "migrated.db"
    config = Config(str(PROJECT_ROOT / "alembic.ini"))
    config.set_main_option("script_location", str(PROJECT_ROOT / "alembic"))
    config.set_main_option("sqlalchemy.url", f"sqlite:///{database}")

    command.upgrade(config, "head")

    engine = create_engine(f"sqlite:///{database}")
    tables = inspect(engine).get_table_names()
    assert "links" in tables
    engine.dispose()
