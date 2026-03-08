import sqlite3

import pytest

import db.connection as db_connection


@pytest.fixture(autouse=True)
def reset_connection():
    if db_connection._connection is not None:
        db_connection._connection.close()
    db_connection._connection = None
    yield
    db_connection.close_connection()


def test_get_connection_returns_sqlite_connection(tmp_path, mocker):
    mocker.patch("db.connection.DB_PATH", str(tmp_path / "test.db"))
    conn = db_connection.get_connection()
    assert isinstance(conn, sqlite3.Connection)


def test_get_connection_singleton(tmp_path, mocker):
    mocker.patch("db.connection.DB_PATH", str(tmp_path / "test.db"))
    conn1 = db_connection.get_connection()
    conn2 = db_connection.get_connection()
    assert conn1 is conn2


def test_get_connection_row_factory(tmp_path, mocker):
    mocker.patch("db.connection.DB_PATH", str(tmp_path / "test.db"))
    conn = db_connection.get_connection()
    assert conn.row_factory == sqlite3.Row


def test_close_connection(tmp_path, mocker):
    mocker.patch("db.connection.DB_PATH", str(tmp_path / "test.db"))
    db_connection.get_connection()
    db_connection.close_connection()
    assert db_connection._connection is None


def test_close_connection_when_none():
    db_connection._connection = None
    db_connection.close_connection()
    assert db_connection._connection is None
