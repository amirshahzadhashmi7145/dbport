"""DBPort API — connection creation (FR-001)."""

from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="DBPort")
_connections: list[dict] = []


class ConnectionCreate(BaseModel):
    name: str = Field(min_length=1)
    dialect: str = Field(min_length=1)
    host: str = Field(min_length=1)
    port: int
    database: str = Field(min_length=1)
    mode: str = Field(min_length=1)
    username: str | None = None
    password: str | None = None


@app.post("/connections", status_code=201)
def create_connection(body: ConnectionCreate) -> dict:
    if len(_connections) >= 50:
        raise HTTPException(status_code=409, detail="connection_limit_reached")
    connection_id = str(uuid4())
    record = {
        "id": connection_id,
        "name": body.name,
        "dialect": body.dialect,
        "host": body.host,
        "port": body.port,
        "database": body.database,
        "mode": body.mode,
        "introspection_status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "status_url": f"/connections/{connection_id}",
    }
    _connections.append(record)
    return record


def reset_store() -> None:
    """Test helper."""

    _connections.clear()
