"""Unit coverage for FR-002 data grid retrieval."""

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


def test_get_table_rows_returns_200_ok() -> None:
    client = TestClient(app)
    connection_id = _create()
    response = client.get(f"/connections/{connection_id}/tables/users/rows")
    assert response.status_code == 200  # Status code is 200 OK


def test_get_table_rows_body_contract() -> None:
    client = TestClient(app)
    connection_id = _create()
    response = client.get(
        f"/connections/{connection_id}/tables/users/rows",
        params={"page": 1, "page_size": 50},
    )
    assert response.status_code == 200
    body = response.json()
    for key in ("rows", "columns", "page", "page_size", "total_rows", "next_cursor"):
        assert key in body, f"missing {key}"
    assert body["page"] == 1
    assert body["page_size"] == 50
    assert body["total_rows"] >= 0
    assert isinstance(body["rows"], list)
    assert isinstance(body["columns"], list)


def test_missing_table_returns_404() -> None:
    client = TestClient(app)
    connection_id = _create()
    response = client.get(f"/connections/{connection_id}/tables/missing/rows")
    assert response.status_code == 404
    assert response.json()["detail"] == "table_not_found"
