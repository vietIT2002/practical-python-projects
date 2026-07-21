"""Atomic JSON persistence for contacts."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

from .errors import StorageError
from .models import Contact


def load_contacts(path: Path) -> list[Contact]:
    """Load contacts; a missing file is an empty list, malformed data errors."""
    if not path.exists():
        return []
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise StorageError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(raw, list):
        raise StorageError(f"{path} must contain a list of contacts")
    return [Contact.from_dict(item) for item in raw]


def save_contacts(path: Path, contacts: list[Contact]) -> None:
    """Write contacts to ``path`` atomically (temp file + replace)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps([contact.to_dict() for contact in contacts], indent=2)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f".{path.name}.", suffix=".tmp"
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.write("\n")
        temporary_path.replace(path)
    except BaseException:
        temporary_path.unlink(missing_ok=True)
        raise
