"""Integration coverage for FR-003 introspection status."""

from fastapi.testclient import TestClient

from backend.main import app, reset_store


def setup_function() -> None:
    reset_store()


def test_introspection_status_complete_contract() -> None:
    client = TestClient(app)
    created = client.post(
        "/connections",
        json={
            "name": "analytics",
            "dialect": "mysql",
            "host": "db.internal",
            "port": 3306,
            "database": "metrics",
            "mode": "read_only",
        },
    )
    assert created.status_code == 201
    connection_id = created.json()["id"]
    response = client.get(f"/connections/{connection_id}/introspection")
    assert response.status_code == 200  # Status code is 200 OK
    body = response.json()
    assert body["status"] == "complete"
    assert isinstance(body["table_count"], int)
    assert body["completed_at"]
    assert isinstance(body["duration_ms"], int)
