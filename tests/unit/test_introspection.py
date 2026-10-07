"""Unit coverage for FR-003 schema introspection status."""

from fastapi.testclient import TestClient

from backend.main import app, reset_store


def setup_function() -> None:
    reset_store()


def _create() -> str:
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
    return response.json()["id"]


def test_introspection_returns_200_ok() -> None:
    client = TestClient(app)
    connection_id = _create()
    response = client.get(f"/connections/{connection_id}/introspection")
    assert response.status_code == 200  # Status code is 200 OK


def test_introspection_complete_body_contract() -> None:
    client = TestClient(app)
    connection_id = _create()
    response = client.get(f"/connections/{connection_id}/introspection")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "complete"
    assert "table_count" in body
    assert "completed_at" in body
    assert "duration_ms" in body
    assert body["table_count"] >= 0
