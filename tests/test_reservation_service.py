from unittest.mock import MagicMock

import pytest

from services import reservation_service


@pytest.fixture
def fake_conn(mocker):
    mock_conn = mocker.MagicMock()
    mocker.patch(
        "services.reservation_service.get_connection"
    ).return_value.__enter__.return_value = mock_conn
    return mock_conn


@pytest.mark.parametrize(
    "available_copies, rowcount, expected_success, expected_msg",
    [
        (None, 0, False, "Libro non trovato."),
        (2, 1, True, "Prenotazione confermata"),
    ],
)
def test_reserve_book(
    fake_conn, available_copies, rowcount, expected_success, expected_msg
):
    select_result = MagicMock()
    select_result.fetchone.return_value = (
        None
        if available_copies is None
        else {"available_copies": available_copies, "title": "Titolo"}
    )
    update_cursor = MagicMock()
    update_cursor.rowcount = rowcount
    fake_conn.execute.side_effect = [select_result, update_cursor, MagicMock()]

    success, message = reservation_service.reserve_book(user_id=1, book_id=42)

    assert success == expected_success
    assert expected_msg in message


def test_reserve_book_zero_copies(fake_conn):
    select_result = MagicMock()
    select_result.fetchone.return_value = {"available_copies": 0, "title": "Dune"}
    fake_conn.execute.side_effect = [select_result]

    success, message = reservation_service.reserve_book(user_id=1, book_id=42)

    assert success is False
    assert "non ha copie disponibili" in message


def test_reserve_book_race_condition(fake_conn):
    select_result = MagicMock()
    select_result.fetchone.return_value = {"available_copies": 1, "title": "Dune"}
    update_cursor = MagicMock()
    update_cursor.rowcount = 0
    fake_conn.execute.side_effect = [select_result, update_cursor]

    success, message = reservation_service.reserve_book(user_id=1, book_id=42)

    assert success is False
    assert "Nessuna copia disponibile" in message


@pytest.mark.parametrize(
    "row, expected_success, expected_msg",
    [
        (None, False, "Prenotazione non trovata."),
        ({"id": 1, "book_id": 10, "status": "active"}, True, "Prenotazione cancellata"),
    ],
)
def test_cancel_reservation(fake_conn, row, expected_success, expected_msg):
    select_result = MagicMock()
    select_result.fetchone.return_value = row
    fake_conn.execute.side_effect = [select_result, MagicMock(), MagicMock()]

    success, message = reservation_service.cancel_reservation(1, 1)

    assert success == expected_success
    assert expected_msg in message


def test_cancel_reservation_already_cancelled(fake_conn):
    select_result = MagicMock()
    select_result.fetchone.return_value = {
        "id": 1,
        "book_id": 10,
        "status": "cancelled",
    }
    fake_conn.execute.side_effect = [select_result]

    success, message = reservation_service.cancel_reservation(1, 1)

    assert success is False
    assert "già stata cancellata" in message


def test_get_user_reservations_with_results(fake_conn):
    fake_conn.execute.return_value.fetchall.return_value = [
        {
            "id": 1,
            "user_id": 1,
            "book_id": 10,
            "reserved_at": "2025-01-01",
            "status": "active",
            "book_title": "Python",
            "book_author": "Guido",
        }
    ]

    result = reservation_service.get_user_reservations(1)

    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].book_title == "Python"


def test_get_user_reservations_empty(fake_conn):
    fake_conn.execute.return_value.fetchall.return_value = []

    result = reservation_service.get_user_reservations(1)

    assert result == []
