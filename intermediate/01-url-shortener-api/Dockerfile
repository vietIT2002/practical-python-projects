# Minimal container image for the URL Shortener API.
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Pin uv for reproducible builds.
RUN pip install --no-cache-dir uv==0.11.29

# Install runtime dependencies first for better layer caching.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

# Copy the application source and migrations.
COPY . .

# Run as an unprivileged user; give it a writable data directory.
RUN useradd --create-home --uid 1000 appuser \
    && mkdir -p /app/data \
    && chown -R appuser /app
USER appuser

ENV URLSHORTENER_DATABASE_URL=sqlite:////app/data/url_shortener.db
EXPOSE 8000

# Apply migrations, then serve.
CMD ["sh", "-c", "uv run alembic upgrade head && uv run uvicorn --app-dir src url_shortener.main:app --host 0.0.0.0 --port 8000"]
