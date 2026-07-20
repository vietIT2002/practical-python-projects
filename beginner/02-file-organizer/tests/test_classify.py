"""Tests for extension classification and config loading."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from file_organizer.classify import (
    OTHER_CATEGORY,
    category_for,
    default_rules,
    load_rules,
)
from file_organizer.errors import ConfigError


def test_default_rules_map_known_extensions() -> None:
    rules = default_rules()
    assert rules[".jpg"] == "images"
    assert rules[".pdf"] == "documents"


def test_category_for_is_case_insensitive() -> None:
    rules = default_rules()
    assert category_for("PHOTO.JPG", rules) == "images"


def test_unknown_extension_goes_to_other() -> None:
    assert category_for("mystery.xyz", default_rules()) == OTHER_CATEGORY


def test_load_rules_none_returns_defaults() -> None:
    assert load_rules(None) == default_rules()


def test_load_rules_from_config(tmp_path: Path) -> None:
    config = tmp_path / "categories.json"
    config.write_text(json.dumps({"notes": [".md", ".TXT"]}), encoding="utf-8")
    rules = load_rules(config)
    assert rules[".md"] == "notes"
    assert rules[".txt"] == "notes"  # normalised to lowercase


def test_load_rules_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ConfigError, match="not found"):
        load_rules(tmp_path / "nope.json")


def test_load_rules_invalid_json(tmp_path: Path) -> None:
    config = tmp_path / "bad.json"
    config.write_text("{ not json", encoding="utf-8")
    with pytest.raises(ConfigError, match="not valid JSON"):
        load_rules(config)


def test_load_rules_not_object(tmp_path: Path) -> None:
    config = tmp_path / "list.json"
    config.write_text("[]", encoding="utf-8")
    with pytest.raises(ConfigError, match="object of category"):
        load_rules(config)


def test_load_rules_unsafe_category(tmp_path: Path) -> None:
    config = tmp_path / "evil.json"
    config.write_text(json.dumps({"../escape": [".x"]}), encoding="utf-8")
    with pytest.raises(ConfigError, match="unsafe category"):
        load_rules(config)


def test_load_rules_extensions_not_list(tmp_path: Path) -> None:
    config = tmp_path / "bad.json"
    config.write_text(json.dumps({"images": ".jpg"}), encoding="utf-8")
    with pytest.raises(ConfigError, match="list of extensions"):
        load_rules(config)
