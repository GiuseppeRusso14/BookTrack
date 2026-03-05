import sqlite3
from unittest.mock import patch

from services import auth_service


def _make_conn():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL UNIQUE,
            password  TEXT    NOT NULL,
            full_name TEXT    NOT NULL
        )
        """
    )
    conn.execute(
        "INSERT INTO users (username, password, full_name) VALUES ('mario', 'pass1', 'Mario Rossi')"
    )
    conn.execute(
        "INSERT INTO users (username, password, full_name) VALUES ('laura', 'pass2', 'Laura Bianchi')"
    )
    conn.commit()
    return conn


def test_authenticate_success():
    conn = _make_conn()
    with patch("services.auth_service.get_connection", return_value=conn):
        user = auth_service.authenticate("mario", "pass1")
    assert user is not None
    assert user.username == "mario"
    assert user.full_name == "Mario Rossi"
    assert user.password == "pass1"
    assert user.id == 1


def test_authenticate_wrong_password():
    conn = _make_conn()
    with patch("services.auth_service.get_connection", return_value=conn):
        user = auth_service.authenticate("mario", "wrong")
    assert user is None


def test_authenticate_unknown_user():
    conn = _make_conn()
    with patch("services.auth_service.get_connection", return_value=conn):
        user = auth_service.authenticate("ghost", "pass1")
    assert user is None


def test_authenticate_empty_credentials():
    conn = _make_conn()
    with patch("services.auth_service.get_connection", return_value=conn):
        user = auth_service.authenticate("", "")
    assert user is None


def test_get_all_usernames_returns_list():
    conn = _make_conn()
    with patch("services.auth_service.get_connection", return_value=conn):
        usernames = auth_service.get_all_usernames()
    assert "mario" in usernames
    assert "laura" in usernames
    assert len(usernames) == 2


def test_get_all_usernames_sorted():
    conn = _make_conn()
    with patch("services.auth_service.get_connection", return_value=conn):
        usernames = auth_service.get_all_usernames()
    assert usernames == sorted(usernames)


def test_get_all_usernames_empty_table():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            full_name TEXT NOT NULL
        )
        """
    )
    conn.commit()
    with patch("services.auth_service.get_connection", return_value=conn):
        usernames = auth_service.get_all_usernames()
    assert usernames == []
