"""End-to-end API tests using an isolated temporary database."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

from url_shortener.infrastructure.models import Link


def test_create_generated_link(client: TestClient) -> None:
    response = client.post("/api/links", json={"url": "https://example.com/page"})
    assert response.status_code == 201
    body = response.json()
    assert body["url"] == "https://example.com/page"
    assert body["clicks"] == 0
    assert body["code"]
    assert body["short_url"].endswith(body["code"])


def test_create_custom_alias(client: TestClient) -> None:
    response = client.post(
        "/api/links", json={"url": "https://example.com", "alias": "mydocs"}
    )
    assert response.status_code == 201
    assert response.json()["code"] == "mydocs"


def test_duplicate_alias_conflicts(client: TestClient) -> None:
    payload = {"url": "https://example.com", "alias": "dup"}
    assert client.post("/api/links", json=payload).status_code == 201
    conflict = client.post("/api/links", json=payload)
    assert conflict.status_code == 409
    assert "detail" in conflict.json()


def test_invalid_scheme_rejected(client: TestClient) -> None:
    response = client.post("/api/links", json={"url": "ftp://example.com"})
    assert response.status_code == 422


def test_empty_url_rejected(client: TestClient) -> None:
    assert client.post("/api/links", json={"url": ""}).status_code == 422


def test_invalid_alias_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/links", json={"url": "https://example.com", "alias": "no spaces!"}
    )
    assert response.status_code == 422


def test_reserved_alias_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/links", json={"url": "https://example.com", "alias": "docs"}
    )
    assert response.status_code == 422


def test_naive_expiration_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/links",
        json={"url": "https://example.com", "expires_at": "2999-01-01T00:00:00"},
    )
    assert response.status_code == 422


def test_past_expiration_rejected(client: TestClient) -> None:
    response = client.post(
        "/api/links",
        json={"url": "https://example.com", "expires_at": "2000-01-01T00:00:00+00:00"},
    )
    assert response.status_code == 422


def test_redirect_and_click_increment(client: TestClient) -> None:
    code = client.post("/api/links", json={"url": "https://example.com/x"}).json()[
        "code"
    ]
    redirect = client.get(f"/{code}", follow_redirects=False)
    assert redirect.status_code == 307
    assert redirect.headers["location"] == "https://example.com/x"

    metadata = client.get(f"/api/links/{code}").json()
    assert metadata["clicks"] == 1


def test_missing_link_returns_404(client: TestClient) -> None:
    assert client.get("/api/links/nope").status_code == 404
    assert client.get("/nope", follow_redirects=False).status_code == 404


def test_expired_link_returns_410(client: TestClient) -> None:
    # Insert an already-expired link directly (the API rejects past expiries).
    factory = client.app.state.session_factory  # type: ignore[attr-defined]
    with factory() as db:
        db.add(
            Link(
                code="old",
                url="https://example.com",
                clicks=0,
                created_at=datetime.now(UTC) - timedelta(days=2),
                expires_at=datetime.now(UTC) - timedelta(days=1),
            )
        )
        db.commit()
    assert client.get("/api/links/old").status_code == 410
    assert client.get("/old", follow_redirects=False).status_code == 410


def test_health(client: TestClient) -> None:
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["database"] == "ok"
