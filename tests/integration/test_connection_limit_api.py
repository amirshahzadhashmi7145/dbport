"""Integration coverage for FR-005 connection limit."""

from fastapi.testclient import TestClient

from backend.main import app, reset_store


def setup_function() -> None:
    reset_store()


def test_get_connections_total_at_most_50() -> None:
    client = TestClient(app)
    for i in range(3):
        response = client.post(
            "/connections",
            json={
                "name": f"c{i}",
                "dialect": "postgresql",
                "host": "127.0.0.1",
                "port": 5432,
                "database": "app",
                "mode": "read_only",
            },
        )
        assert response.status_code == 201
    listed = client.get("/connections")
    assert listed.status_code == 200
    body = listed.json()
    assert body["total"] <= 50
    assert body["total"] == 3
    assert body["limit"] == 50


def test_51st_connection_returns_409() -> None:
    client = TestClient(app)
    for i in range(50):
        response = client.post(
            "/connections",
            json={
                "name": f"c{i}",
                "dialect": "postgresql",
                "host": "127.0.0.1",
                "port": 5432,
                "database": "app",
                "mode": "read_only",
            },
        )
        assert response.status_code == 201, response.text
    response = client.post(
        "/connections",
        json={
            "name": "overflow",
            "dialect": "postgresql",
            "host": "127.0.0.1",
            "port": 5432,
            "database": "app",
            "mode": "read_only",
        },
    )
    assert response.status_code == 409
    assert response.json()["detail"] == "connection_limit_reached"
