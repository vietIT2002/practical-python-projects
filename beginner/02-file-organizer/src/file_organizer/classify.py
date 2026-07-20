"""Map file extensions to category folders.

The default rules cover common file types. A user can override them with a JSON
config file of the form ``{"category": [".ext", ...]}``.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .errors import ConfigError

#: Files whose extension is unknown go here.
OTHER_CATEGORY = "other"

#: A category must be a single, safe path component (no separators or "..").
_SAFE_CATEGORY = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 _-]*$")

DEFAULT_CATEGORIES: dict[str, tuple[str, ...]] = {
    "images": (".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"),
    "documents": (".pdf", ".doc", ".docx", ".txt", ".md", ".rtf", ".odt"),
    "spreadsheets": (".xls", ".xlsx", ".csv", ".ods"),
    "archives": (".zip", ".tar", ".gz", ".bz2", ".7z", ".rar"),
    "audio": (".mp3", ".wav", ".flac", ".ogg", ".m4a"),
    "video": (".mp4", ".mkv", ".mov", ".avi", ".webm"),
    "code": (".py", ".js", ".ts", ".java", ".c", ".cpp", ".rs", ".go", ".rb", ".sh"),
}


def _rules_from_categories(categories: dict[str, Any]) -> dict[str, str]:
    """Build an extension→category lookup, validating category names."""
    rules: dict[str, str] = {}
    for category, extensions in categories.items():
        if not _SAFE_CATEGORY.match(category):
            raise ConfigError(
                f"unsafe category name {category!r}; use letters, numbers, spaces, "
                "hyphens, or underscores only"
            )
        if not isinstance(extensions, (list, tuple)):
            raise ConfigError(f"category {category!r} must map to a list of extensions")
        for extension in extensions:
            rules[str(extension).lower()] = category
    return rules


def default_rules() -> dict[str, str]:
    """Return the built-in extension→category rules."""
    return _rules_from_categories(dict(DEFAULT_CATEGORIES))


def load_rules(config_path: Path | None) -> dict[str, str]:
    """Load rules from a JSON config file, or return the defaults if ``None``."""
    if config_path is None:
        return default_rules()
    try:
        raw = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ConfigError(f"config file not found: {config_path}") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"{config_path} is not valid JSON: {exc}") from exc
    if not isinstance(raw, dict):
        raise ConfigError(f"{config_path} must be an object of category to extensions")
    return _rules_from_categories(raw)


def category_for(name: str, rules: dict[str, str]) -> str:
    """Return the category for a file name based on its extension."""
    extension = Path(name).suffix.lower()
    return rules.get(extension, OTHER_CATEGORY)
