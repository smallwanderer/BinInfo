"""Local SQLite-backed audit log for Streamlit literature searches."""
from __future__ import annotations

import json
import os
import sqlite3
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_DEFAULT_DB_PATH = Path(__file__).resolve().parents[2] / "data" / "usage.db"

_CREATE_TABLE_SQL = """
    CREATE TABLE IF NOT EXISTS search_usage (
        request_id TEXT PRIMARY KEY,
        created_at TEXT NOT NULL,
        completed_at TEXT,
        user_id TEXT,
        search_mode TEXT NOT NULL,
        query TEXT NOT NULL,
        parameters_json TEXT NOT NULL,
        status TEXT NOT NULL CHECK (status IN ('running', 'completed', 'failed')),
        result_count INTEGER,
        elapsed_ms INTEGER,
        result_json TEXT,
        error_type TEXT,
        error_message TEXT
    )
"""


def database_path() -> Path:
    """Return the configured usage database path.

    BIOINFO_USAGE_DB_PATH is useful when the app is run from a container or
    when the log should live on a separately backed-up drive.
    """
    configured = os.getenv("BIOINFO_USAGE_DB_PATH")
    return Path(configured).expanduser() if configured else _DEFAULT_DB_PATH


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, default=str)


def _connect() -> sqlite3.Connection:
    path = database_path()
    path.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(path, timeout=10)
    connection.execute("PRAGMA journal_mode=WAL")
    connection.execute("PRAGMA busy_timeout=10000")
    connection.execute(_CREATE_TABLE_SQL)

    # Migrate databases created by the previous session-scoped logger. The
    # transaction preserves every persistent search field and only removes
    # the no-longer-used session_id column.
    columns = {
        row[1] for row in connection.execute("PRAGMA table_info(search_usage)").fetchall()
    }
    if "session_id" in columns:
        connection.execute("BEGIN IMMEDIATE")
        connection.execute("DROP TABLE IF EXISTS search_usage_without_session")
        connection.execute(
            _CREATE_TABLE_SQL.replace("search_usage", "search_usage_without_session")
        )
        persistent_columns = (
            "request_id, created_at, completed_at, user_id, search_mode, query, "
            "parameters_json, status, result_count, elapsed_ms, result_json, "
            "error_type, error_message"
        )
        connection.execute(
            f"INSERT INTO search_usage_without_session ({persistent_columns}) "
            f"SELECT {persistent_columns} FROM search_usage"
        )
        connection.execute("DROP TABLE search_usage")
        connection.execute(
            "ALTER TABLE search_usage_without_session RENAME TO search_usage"
        )
        connection.commit()

    connection.execute(
        "CREATE INDEX IF NOT EXISTS idx_search_usage_created_at "
        "ON search_usage(created_at)"
    )
    return connection


def start_search(
    *,
    user_id: str | None,
    search_mode: str,
    query: str,
    parameters: dict[str, Any] | None = None,
) -> str:
    """Insert a running search and return its unique request ID."""
    request_id = str(uuid.uuid4())
    with _connect() as connection:
        connection.execute(
            """
            INSERT INTO search_usage (
                request_id, created_at, user_id, search_mode,
                query, parameters_json, status
            ) VALUES (?, ?, ?, ?, ?, ?, 'running')
            """,
            (
                request_id,
                _utc_now(),
                user_id,
                search_mode,
                query,
                _json(parameters or {}),
            ),
        )
    return request_id


def complete_search(
    request_id: str,
    *,
    result_count: int,
    elapsed_ms: int,
    result: Any,
) -> None:
    """Mark a search complete and persist its JSON-serializable result."""
    with _connect() as connection:
        connection.execute(
            """
            UPDATE search_usage
            SET completed_at = ?, status = 'completed', result_count = ?,
                elapsed_ms = ?, result_json = ?, error_type = NULL,
                error_message = NULL
            WHERE request_id = ?
            """,
            (_utc_now(), result_count, elapsed_ms, _json(result), request_id),
        )


def fail_search(request_id: str, *, elapsed_ms: int, error: Exception) -> None:
    """Mark a search failed without storing a traceback or secret-bearing data."""
    with _connect() as connection:
        connection.execute(
            """
            UPDATE search_usage
            SET completed_at = ?, status = 'failed', elapsed_ms = ?,
                error_type = ?, error_message = ?
            WHERE request_id = ?
            """,
            (
                _utc_now(),
                elapsed_ms,
                type(error).__name__,
                str(error)[:1000],
                request_id,
            ),
        )


def list_searches(
    *,
    limit: int = 200,
    status: str | None = None,
    search_mode: str | None = None,
    query_contains: str | None = None,
) -> list[dict[str, Any]]:
    """Return recent records without the potentially large result JSON."""
    conditions: list[str] = []
    parameters: list[Any] = []

    if status:
        conditions.append("status = ?")
        parameters.append(status)
    if search_mode:
        conditions.append("search_mode = ?")
        parameters.append(search_mode)
    if query_contains:
        conditions.append("query LIKE ?")
        parameters.append(f"%{query_contains}%")

    where = f"WHERE {' AND '.join(conditions)}" if conditions else ""
    parameters.append(max(1, min(limit, 5000)))

    with _connect() as connection:
        connection.row_factory = sqlite3.Row
        rows = connection.execute(
            f"""
            SELECT request_id, created_at, completed_at, user_id, search_mode,
                   query, status, result_count, elapsed_ms, error_type
            FROM search_usage
            {where}
            ORDER BY created_at DESC
            LIMIT ?
            """,
            parameters,
        ).fetchall()
    return [dict(row) for row in rows]


def get_search(request_id: str) -> dict[str, Any] | None:
    """Return one complete record, decoding its stored JSON fields."""
    with _connect() as connection:
        connection.row_factory = sqlite3.Row
        row = connection.execute(
            "SELECT * FROM search_usage WHERE request_id = ?",
            (request_id,),
        ).fetchone()

    if row is None:
        return None

    record = dict(row)
    for key in ("parameters_json", "result_json"):
        raw_value = record.pop(key, None)
        output_key = key.removesuffix("_json")
        if raw_value is None:
            record[output_key] = None
            continue
        try:
            record[output_key] = json.loads(raw_value)
        except json.JSONDecodeError:
            record[output_key] = raw_value
    return record
