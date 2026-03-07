import sqlite3
from unittest.mock import patch

import pytest

from services import auth_service


@pytest.fixture
def conn():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute(
        """
        CREATE TABLE users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL UNIQUE,
            password  TEXT    NOT NULL,
            full_name TEXT    NOT NULL
        )
        """
    )
    db.execute("INSERT INTO users (username, password, full_name) VALUES ('mario', 'pass1', 'Mario Rossi')")
    db.execute("INSERT INTO users (username, password, full_name) VALUES ('laura', 'pass2', 'Laura Bianchi')")
    db.commit()
    return db


@pytest.fixture
def empty_conn():
    db = sqlite3.connect(":memory:")
    db.row_factory = sqlite3.Row
    db.execute(
        """
        CREATE TABLE users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL UNIQUE,
            password  TEXT    NOT NULL,
            full_name TEXT    NOT NULL
        )
        """
    )
    db.commit()
    return db


def test_authenticate_success(conn):
    with patch("services.auth_service.get_connection", return_value=conn):
        user = auth_service.authenticate("mario", "pass1")
    assert user is not None
    assert user.username == "mario"
    assert user.full_name == "Mario Rossi"


def test_authenticate_wrong_password(conn):
    with patch("services.auth_service.get_connection", return_value=conn):
        user = auth_service.authenticate("mario", "wrong")
    assert user is None


def test_authenticate_unknown_user(conn):
    with patch("services.auth_service.get_connection", return_value=conn):
        user = auth_service.authenticate("ghost", "pass1")
    assert user is None


def test_get_all_usernames_returns_sorted_list(conn):
    with patch("services.auth_service.get_connection", return_value=conn):
        usernames = auth_service.get_all_usernames()
    assert usernames == ["laura", "mario"]


def test_get_all_usernames_empty_table(empty_conn):
    with patch("services.auth_service.get_connection", return_value=empty_conn):
        usernames = auth_service.get_all_usernames()
    assert usernames == []
