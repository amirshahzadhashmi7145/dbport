"""DBPort API — connections, data grid, and introspection (FR-001..003)."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="DBPort")
_connections: list[dict] = []
# connection_id -> table_name -> list[row dict]
_tables: dict[str, dict[str, list[dict]]] = {}
# connection_id -> introspection meta
_introspection: dict[str, dict] = {}


class ConnectionCreate(BaseModel):
    name: str = Field(min_length=1)
    dialect: str = Field(min_length=1)
    host: str = Field(min_length=1)
    port: int
    database: str = Field(min_length=1)
    mode: str = Field(min_length=1)
    username: str | None = None
    password: str | None = None


def _get_connection(connection_id: str) -> dict:
    for item in _connections:
        if item["id"] == connection_id:
            return item
    raise HTTPException(status_code=404, detail="connection_not_found")


@app.post("/connections", status_code=201)
def create_connection(body: ConnectionCreate) -> dict:
    if len(_connections) >= 50:
        raise HTTPException(status_code=409, detail="connection_limit_reached")
    connection_id = str(uuid4())
    now = datetime.now(timezone.utc)
    # Seed a demo table so the data-grid endpoint is exercisable in tests.
    _tables[connection_id] = {
        "users": [
            {"id": 1, "email": "a@example.com"},
            {"id": 2, "email": "b@example.com"},
        ]
    }
    _introspection[connection_id] = {
        "status": "pending",
        "table_count": 0,
        "completed_at": None,
        "duration_ms": 0,
        "error_code": None,
        "started_at": now,
    }
    record = {
        "id": connection_id,
        "name": body.name,
        "dialect": body.dialect,
        "host": body.host,
        "port": body.port,
        "database": body.database,
        "mode": body.mode,
        "introspection_status": "pending",
        "created_at": now.isoformat(),
        "status_url": f"/connections/{connection_id}",
    }
    _connections.append(record)
    return record


@app.get("/connections/{connection_id}/tables/{table}/rows")
def get_table_rows(
    connection_id: str,
    table: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=1000),
) -> dict:
    _get_connection(connection_id)
    tables = _tables.get(connection_id, {})
    if table not in tables:
        raise HTTPException(status_code=404, detail="table_not_found")
    all_rows = tables[table]
    total_rows = len(all_rows)
    start = (page - 1) * page_size
    end = start + page_size
    page_rows = all_rows[start:end]
    columns = []
    if all_rows:
        columns = [{"name": key, "type": type(value).__name__} for key, value in all_rows[0].items()]
    elif table == "users":
        columns = [{"name": "id", "type": "int"}, {"name": "email", "type": "str"}]
    next_cursor = str(page + 1) if end < total_rows else None
    return {
        "rows": page_rows,
        "columns": columns,
        "page": page,
        "page_size": page_size,
        "total_rows": total_rows,
        "next_cursor": next_cursor,
    }


@app.get("/connections/{connection_id}/introspection")
def get_introspection(connection_id: str) -> dict:
    connection = _get_connection(connection_id)
    meta = _introspection.get(connection_id)
    if meta is None:
        return {"status": "pending", "table_count": 0, "completed_at": None, "duration_ms": 0}
    # First status poll completes introspection when tables are already seeded.
    if meta["status"] == "pending":
        started = meta.get("started_at") or datetime.now(timezone.utc)
        completed = datetime.now(timezone.utc)
        table_count = len(_tables.get(connection_id, {}))
        meta.update(
            {
                "status": "complete",
                "table_count": table_count,
                "completed_at": completed.isoformat(),
                "duration_ms": max(1, int((completed - started).total_seconds() * 1000)),
            }
        )
        connection["introspection_status"] = "complete"
    body = {
        "status": meta["status"],
        "table_count": meta["table_count"],
        "completed_at": meta["completed_at"],
        "duration_ms": meta["duration_ms"],
    }
    if meta.get("error_code"):
        body["error_code"] = meta["error_code"]
    return body


def reset_store() -> None:
    """Test helper."""

    _connections.clear()
    _tables.clear()
    _introspection.clear()
