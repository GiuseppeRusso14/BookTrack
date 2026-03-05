from unittest.mock import MagicMock, patch

import db.connection as db_mod


def setup_function():
    db_mod._connection = None


def teardown_function():
    db_mod._connection = None


def test_get_connection_creates_new():
    with patch("db.connection.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        conn = db_mod.get_connection()
    assert conn is mock_conn
    mock_connect.assert_called_once()


def test_get_connection_reuses_existing():
    with patch("db.connection.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        conn1 = db_mod.get_connection()
        conn2 = db_mod.get_connection()
    assert conn1 is conn2
    mock_connect.assert_called_once()


def test_get_connection_sets_row_factory():
    with patch("db.connection.sqlite3.connect") as mock_connect:
        import sqlite3

        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        db_mod.get_connection()
    assert mock_conn.row_factory == sqlite3.Row


def test_get_connection_enables_foreign_keys():
    with patch("db.connection.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        db_mod.get_connection()
    mock_conn.execute.assert_called_with("PRAGMA foreign_keys = ON")


def test_close_connection_clears_state():
    with patch("db.connection.sqlite3.connect") as mock_connect:
        mock_conn = MagicMock()
        mock_connect.return_value = mock_conn
        db_mod.get_connection()
    db_mod.close_connection()
    assert db_mod._connection is None
    mock_conn.close.assert_called_once()


def test_close_connection_when_none():
    db_mod._connection = None
    db_mod.close_connection()
    assert db_mod._connection is None
