"""CSV export for contacts."""

from __future__ import annotations

import csv
from pathlib import Path

from .errors import ExportError
from .models import Contact

FIELDNAMES = ("id", "name", "email", "phone")


def export_to_csv(contacts: list[Contact], path: Path, *, force: bool = False) -> None:
    """Write contacts to ``path`` as CSV.

    Refuses to overwrite an existing file unless ``force`` is set, so an export
    never destroys data by accident.
    """
    if path.exists() and not force:
        raise ExportError(f"{path} already exists; pass force to overwrite")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(
                {
                    "id": contact.id,
                    "name": contact.name,
                    "email": contact.email or "",
                    "phone": contact.phone or "",
                }
            )
