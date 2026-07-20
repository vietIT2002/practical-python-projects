"""Application factory and domain-error handlers."""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from .api.routes import router
from .domain.errors import (
    AliasConflictError,
    CodeGenerationError,
    LinkExpiredError,
    LinkNotFoundError,
)
from .infrastructure.db import build_engine, build_session_factory
from .settings import Settings, get_settings

# Maps each domain error to an HTTP status code. All produce the same body shape.
_ERROR_STATUS: dict[type[Exception], int] = {
    LinkNotFoundError: status.HTTP_404_NOT_FOUND,
    LinkExpiredError: status.HTTP_410_GONE,
    AliasConflictError: status.HTTP_409_CONFLICT,
    CodeGenerationError: status.HTTP_503_SERVICE_UNAVAILABLE,
}

_ERROR_MESSAGE: dict[type[Exception], str] = {
    LinkNotFoundError: "No link exists for that code.",
    LinkExpiredError: "This link has expired.",
    AliasConflictError: "That alias is already taken.",
    CodeGenerationError: "Could not allocate a unique code; please retry.",
}


def create_app(settings: Settings | None = None) -> FastAPI:
    """Build a configured FastAPI application."""
    settings = settings or get_settings()
    engine = build_engine(settings.database_url)

    app = FastAPI(
        title="URL Shortener API",
        version="0.1.0",
        summary="Create short links and redirect to their destinations.",
    )
    app.state.settings = settings
    app.state.engine = engine
    app.state.session_factory = build_session_factory(engine)
    app.include_router(router)
    _register_error_handlers(app)
    return app


def _register_error_handlers(app: FastAPI) -> None:
    async def handle_domain_error(_: Request, exc: Exception) -> JSONResponse:
        status_code = _ERROR_STATUS.get(
            type(exc), status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        message = _ERROR_MESSAGE.get(type(exc), "Unexpected error.")
        return JSONResponse(status_code=status_code, content={"detail": message})

    for error_type in _ERROR_STATUS:
        app.add_exception_handler(error_type, handle_domain_error)


# Uvicorn entry point: `uvicorn url_shortener.main:app`
app = create_app()
