"""Read and write the operation manifest used to undo an applied run."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any

from .errors import ManifestError
from .models import Move

MANIFEST_VERSION = 1
DEFAULT_MANIFEST_NAME = "file-organizer-manifest.json"


def save_manifest(path: Path, moves: tuple[Move, ...]) -> None:
    """Write the completed moves to ``path`` atomically."""
    payload = json.dumps(
        {
            "version": MANIFEST_VERSION,
            "moves": [
                {
                    "source": os.fspath(move.source),
                    "destination": os.fspath(move.destination),
                    "category": move.category,
                }
                for move in moves
            ],
        },
        indent=2,
    )
    path.parent.mkdir(parents=True, exist_ok=True)
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


def load_manifest(path: Path) -> list[Move]:
    """Load moves from a manifest file, raising :class:`ManifestError` if bad."""
    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise ManifestError(f"manifest not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise ManifestError(f"{path} is not valid JSON: {exc}") from exc

    if not isinstance(raw, dict) or "moves" not in raw:
        raise ManifestError(f"{path} is not a valid manifest")

    moves: list[Move] = []
    for item in raw["moves"]:
        try:
            moves.append(
                Move(
                    source=Path(item["source"]),
                    destination=Path(item["destination"]),
                    category=str(item["category"]),
                )
            )
        except (KeyError, TypeError) as exc:
            raise ManifestError(f"{path} has a malformed move entry: {exc}") from exc
    return moves
