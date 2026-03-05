import sqlite3
from unittest.mock import patch

from db import seed


def _make_empty_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    return conn


def test_initialize_database_creates_tables():
    conn = _make_empty_conn()
    with patch("db.seed.get_connection", return_value=conn):
        seed.initialize_database()
    tables = {
        row[0]
        for row in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()
    }
    assert "users" in tables
    assert "books" in tables
    assert "reservations" in tables


def test_initialize_database_idempotent():
    conn = _make_empty_conn()
    with patch("db.seed.get_connection", return_value=conn):
        seed.initialize_database()
        seed.initialize_database()  # second call must not raise


def test_seed_users_inserts_five_users():
    conn = _make_empty_conn()
    with patch("db.seed.get_connection", return_value=conn):
        seed.initialize_database()
    seed._seed_users(conn)
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert count == 5


def test_seed_users_skips_when_already_seeded():
    conn = _make_empty_conn()
    with patch("db.seed.get_connection", return_value=conn):
        seed.initialize_database()
    seed._seed_users(conn)
    seed._seed_users(conn)  # second call must not duplicate
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    assert count == 5


def test_seed_users_correct_data():
    conn = _make_empty_conn()
    with patch("db.seed.get_connection", return_value=conn):
        seed.initialize_database()
    seed._seed_users(conn)
    usernames = [
        row[0] for row in conn.execute("SELECT username FROM users").fetchall()
    ]
    assert "mario_rossi" in usernames
    assert "laura_bianchi" in usernames
