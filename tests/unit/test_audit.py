"""Unit coverage for FR-004 audit timing."""

from fastapi.testclient import TestClient

from backend.main import app, reset_store, _audit


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
            "mode": "read_write",
        },
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_write_records_audit_before_response() -> None:
    client = TestClient(app)
    connection_id = _create()
    response = client.post(
        f"/connections/{connection_id}/tables/users/rows",
        json={"values": {"id": 3, "email": "c@example.com"}},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["audit_entry_id"]
    assert any(entry["id"] == body["audit_entry_id"] and entry["status"] == "succeeded" for entry in _audit)
    # Audit committed before response: entry exists and succeeded with the write
    assert _audit[-1]["operation"] == "insert"
    assert _audit[-1]["affected_rows"] == 1


def test_no_window_without_audit() -> None:
    """FR-004/AC-2: write response includes audit_entry_id already committed."""
    client = TestClient(app)
    connection_id = _create()
    before = len(_audit)
    response = client.post(
        f"/connections/{connection_id}/tables/users/rows",
        json={"values": {"id": 9, "email": "z@example.com"}},
    )
    assert response.status_code == 201
    assert len(_audit) == before + 1
    assert response.json()["audit_entry_id"] == _audit[-1]["id"]
    assert _audit[-1]["status"] == "succeeded"  # committed before API response
