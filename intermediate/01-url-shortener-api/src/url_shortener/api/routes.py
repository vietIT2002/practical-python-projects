"""HTTP routes.

The catch-all redirect ``/{code}`` is registered last so that specific routes
like ``/health`` and ``/api/links`` are matched first.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from ..infrastructure.models import Link
from .dependencies import ServiceDep
from .schemas import CreateLinkRequest, HealthResponse, LinkResponse

router = APIRouter()


def _aware(value: datetime | None) -> datetime | None:
    if value is None:
        return None
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


def _to_response(link: Link, base_url: str) -> LinkResponse:
    return LinkResponse(
        code=link.code,
        short_url=f"{base_url.rstrip('/')}/{link.code}",
        url=link.url,
        clicks=link.clicks,
        created_at=_aware(link.created_at) or link.created_at,
        expires_at=_aware(link.expires_at),
    )


@router.post(
    "/api/links",
    status_code=status.HTTP_201_CREATED,
    response_model=LinkResponse,
    tags=["links"],
)
def create_link(
    payload: CreateLinkRequest,
    request: Request,
    service: ServiceDep,
) -> LinkResponse:
    link = service.create_link(
        url=str(payload.url), alias=payload.alias, expires_at=payload.expires_at
    )
    return _to_response(link, request.app.state.settings.base_url)


@router.get("/api/links/{code}", response_model=LinkResponse, tags=["links"])
def read_link(
    code: str,
    request: Request,
    service: ServiceDep,
) -> LinkResponse:
    link = service.get_link(code)
    return _to_response(link, request.app.state.settings.base_url)


@router.get("/health", response_model=HealthResponse, tags=["health"])
def health(request: Request) -> HealthResponse:
    engine = request.app.state.engine
    database = "ok"
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except SQLAlchemyError:
        database = "error"
    return HealthResponse(
        status="ok" if database == "ok" else "degraded", database=database
    )


@router.get("/{code}", tags=["redirect"])
def redirect(code: str, service: ServiceDep) -> RedirectResponse:
    destination = service.redirect(code)
    return RedirectResponse(destination, status_code=status.HTTP_307_TEMPORARY_REDIRECT)
