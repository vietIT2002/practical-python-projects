"""Tests for CSV export."""

from __future__ import annotations

import csv
from pathlib import Path

import pytest

from contact_book.errors import ExportError
from contact_book.export import export_to_csv
from contact_book.models import Contact


def _contacts() -> list[Contact]:
    return [
        Contact("1", "Ada", "ada@example.com", "5551234567"),
        Contact("2", "Alan", None, None),
    ]


def test_export_writes_header_and_rows(tmp_path: Path) -> None:
    path = tmp_path / "out.csv"
    export_to_csv(_contacts(), path)
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    assert [r["name"] for r in rows] == ["Ada", "Alan"]
    assert rows[1]["email"] == ""  # missing optional rendered empty


def test_export_refuses_to_overwrite(tmp_path: Path) -> None:
    path = tmp_path / "out.csv"
    path.write_text("existing", encoding="utf-8")
    with pytest.raises(ExportError, match="already exists"):
        export_to_csv(_contacts(), path)


def test_export_force_overwrites(tmp_path: Path) -> None:
    path = tmp_path / "out.csv"
    path.write_text("existing", encoding="utf-8")
    export_to_csv(_contacts(), path, force=True)
    assert "Ada" in path.read_text(encoding="utf-8")


def test_export_creates_parent_dir(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "out.csv"
    export_to_csv(_contacts(), path)
    assert path.is_file()
