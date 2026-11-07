"""SQLite fixture database containing synthetic community access events."""

import os
import sqlite3


SAMPLE_ROWS = [
    ("VA-001", "voluntario_azul", "voluntario", "centro_comunitario"),
    ("VA-002", "tecnico_verde", "tecnico", "escola_municipal"),
    ("VA-003", "operador_sol", "operador", "ubs"),
]


def connect(path=None):
    path = path or os.environ.get("DATABASE_PATH", "/tmp/vila_aurora.sqlite3")
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def initialize(path=None):
    connection = connect(path)
    try:
        connection.execute(
            "CREATE TABLE IF NOT EXISTS access_events "
            "(event_id TEXT PRIMARY KEY, alias TEXT NOT NULL, role TEXT NOT NULL, site TEXT NOT NULL)"
        )
        connection.executemany(
            "INSERT OR IGNORE INTO access_events VALUES (?, ?, ?, ?)", SAMPLE_ROWS
        )
        connection.commit()
    finally:
        connection.close()


def vulnerable_search(query, path=None):
    """Intentionally unsafe teaching example. Never expose outside this lab."""
    connection = connect(path)
    try:
        sql = (
            "SELECT event_id, alias, role, site FROM access_events "
            f"WHERE alias LIKE '%{query}%'"
        )
        return [dict(row) for row in connection.execute(sql).fetchall()]
    finally:
        connection.close()


def fixed_search(query, path=None):
    """Safe equivalent: treat user input strictly as a query value."""
    connection = connect(path)
    try:
        sql = "SELECT event_id, alias, role, site FROM access_events WHERE alias LIKE ?"
        return [dict(row) for row in connection.execute(sql, (f"%{query}%",)).fetchall()]
    finally:
        connection.close()
