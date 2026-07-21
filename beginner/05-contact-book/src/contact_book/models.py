"""The typed contact record and its (de)serialisation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .errors import StorageError


@dataclass(frozen=True)
class Contact:
    """A single contact. Email and phone are optional."""

    id: str
    name: str
    email: str | None = None
    phone: str | None = None

    def to_dict(self) -> dict[str, str]:
        record = {"id": self.id, "name": self.name}
        if self.email is not None:
            record["email"] = self.email
        if self.phone is not None:
            record["phone"] = self.phone
        return record

    @classmethod
    def from_dict(cls, data: Any) -> Contact:
        if not isinstance(data, dict):
            raise StorageError(f"expected a contact object, got {type(data).__name__}")
        try:
            identifier = str(data["id"])
            name = str(data["name"])
        except KeyError as exc:
            raise StorageError(f"stored contact is missing field {exc}") from exc
        email = data.get("email")
        phone = data.get("phone")
        return cls(
            id=identifier,
            name=name,
            email=str(email) if email is not None else None,
            phone=str(phone) if phone is not None else None,
        )
