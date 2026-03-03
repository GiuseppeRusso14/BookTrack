import os
import sqlite3
from typing import Optional

DB_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "bookshelf.db"
)

_connection: Optional[sqlite3.Connection] = None

def get_connection() -> sqlite3.Connection:
    global _connection
    if _connection is None:
        _connection = sqlite3.connect(DB_PATH)
        _connection.row_factory = sqlite3.Row
        _connection.execute("PRAGMA foreign_keys = ON")
    return _connection


def close_connection() -> None:
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None