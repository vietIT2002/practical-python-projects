"""Tests for JSON persistence."""

from __future__ import annotations

from pathlib import Path

import pytest

from contact_book import storage
from contact_book.errors import StorageError
from contact_book.models import Contact


def test_missing_file_is_empty(tmp_path: Path) -> None:
    assert storage.load_contacts(tmp_path / "none.json") == []


def test_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "contacts.json"
    contacts = [
        Contact("1", "Ada", "ada@example.com", None),
        Contact("2", "Alan", None, "5551234567"),
    ]
    storage.save_contacts(path, contacts)
    assert storage.load_contacts(path) == contacts


def test_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "c.json"
    path.write_text("{ not json", encoding="utf-8")
    with pytest.raises(StorageError, match="not valid JSON"):
        storage.load_contacts(path)


def test_non_list(tmp_path: Path) -> None:
    path = tmp_path / "c.json"
    path.write_text('{"id": "1"}', encoding="utf-8")
    with pytest.raises(StorageError, match="must contain a list"):
        storage.load_contacts(path)


def test_malformed_item(tmp_path: Path) -> None:
    path = tmp_path / "c.json"
    path.write_text('[{"id": "1"}]', encoding="utf-8")  # missing name
    with pytest.raises(StorageError, match="missing field"):
        storage.load_contacts(path)
