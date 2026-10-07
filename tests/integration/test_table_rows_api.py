"""Integration coverage for FR-002 data grid retrieval."""

from fastapi.testclient import TestClient

from backend.main import app, reset_store


def setup_function() -> None:
    reset_store()


def test_grid_retrieval_200_and_body() -> None:
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
    response = client.get(f"/connections/{connection_id}/tables/users/rows?page=1&page_size=10")
    assert response.status_code == 200  # Status code is 200 OK
    body = response.json()
    assert "rows" in body and "columns" in body
    assert "page" in body and "page_size" in body
    assert "total_rows" in body and "next_cursor" in body
