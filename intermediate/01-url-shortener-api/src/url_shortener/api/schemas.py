"""Request and response models. These define the public API contract."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl, field_validator

#: Custom aliases: 3-32 chars of letters, digits, hyphen, or underscore.
ALIAS_PATTERN = r"^[A-Za-z0-9_-]{3,32}$"

#: Aliases that would collide with the API's own routes.
RESERVED_ALIASES = frozenset({"docs", "redoc", "health"})


class CreateLinkRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "url": "https://example.com/a/very/long/path",
                "alias": "docs",
                "expires_at": "2030-01-01T00:00:00+00:00",
            }
        }
    )

    url: HttpUrl
    alias: str | None = Field(default=None, pattern=ALIAS_PATTERN)
    expires_at: datetime | None = None

    @field_validator("alias")
    @classmethod
    def _not_reserved(cls, value: str | None) -> str | None:
        if value is not None and value.lower() in RESERVED_ALIASES:
            raise ValueError(f"alias {value!r} is reserved")
        return value

    @field_validator("expires_at")
    @classmethod
    def _future_and_aware(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return value
        if value.tzinfo is None:
            raise ValueError("expires_at must include a timezone offset")
        if value <= datetime.now(UTC):
            raise ValueError("expires_at must be in the future")
        return value


class LinkResponse(BaseModel):
    code: str
    short_url: str
    url: str
    clicks: int
    created_at: datetime
    expires_at: datetime | None


class HealthResponse(BaseModel):
    status: str
    database: str
