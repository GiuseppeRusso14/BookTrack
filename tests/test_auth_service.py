import sqlite3
from unittest.mock import patch
import pytest
from services import auth_service

@pytest.fixture
def create_db():
    def _create(users=None):
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
        if users:
            for u in users:
                db.execute(
                    "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
                    (u["username"], u["password"], u["full_name"])
                )
        db.commit()
        yield db
        db.close()
    return _create

@pytest.fixture
def conn(create_db):
    users = [
        {"username": "mario", "password": "pass1", "full_name": "Mario Rossi"},
        {"username": "laura", "password": "pass2", "full_name": "Laura Bianchi"}
    ]
    yield from create_db(users)

@pytest.fixture
def empty_conn(create_db):
    yield from create_db([])

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