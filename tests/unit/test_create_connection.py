"""Unit coverage for FR-001 connection creation."""

from fastapi.testclient import TestClient

from backend.main import app, reset_store


def setup_function() -> None:
    reset_store()


def test_create_connection_returns_201_created() -> None:
    client = TestClient(app)
    response = client.post(
        "/connections",
        json={
            "name": "local",
            "dialect": "postgresql",
            "host": "127.0.0.1",
            "port": 5432,
            "database": "app",
            "mode": "read_only",
        },
    )
    assert response.status_code == 201, response.text
    assert response.status_code == 201  # Status code is 201 Created


def test_create_connection_body_has_required_fields() -> None:
    client = TestClient(app)
    response = client.post(
        "/connections",
        json={
            "name": "local",
            "dialect": "postgresql",
            "host": "127.0.0.1",
            "port": 5432,
            "database": "app",
            "mode": "read_only",
        },
    )
    assert response.status_code == 201
    body = response.json()
    for key in (
        "id",
        "name",
        "dialect",
        "host",
        "port",
        "database",
        "mode",
        "introspection_status",
        "created_at",
        "status_url",
    ):
        assert key in body, f"missing {key}"
    assert "password" not in body
