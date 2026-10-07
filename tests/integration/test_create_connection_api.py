"""Integration coverage for POST /connections (FR-001)."""

from fastapi.testclient import TestClient

from backend.main import app, reset_store


def setup_function() -> None:
    reset_store()


def test_post_connections_201_and_body_contract() -> None:
    client = TestClient(app)
    response = client.post(
        "/connections",
        json={
            "name": "analytics",
            "dialect": "mysql",
            "host": "db.internal",
            "port": 3306,
            "database": "metrics",
            "mode": "read_write",
            "username": "u",
            "password": "secret",
        },
    )
    assert response.status_code == 201  # Status code is 201 Created
    body = response.json()
    assert body["name"] == "analytics"
    assert body["dialect"] == "mysql"
    assert body["host"] == "db.internal"
    assert body["port"] == 3306
    assert body["database"] == "metrics"
    assert body["mode"] == "read_only"
    assert body["introspection_status"] == "pending"
    assert body["id"]
    assert body["created_at"]
    assert body["status_url"] == f"/connections/{body['id']}"
    assert "password" not in body
