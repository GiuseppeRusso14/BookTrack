import pytest
from services.reservation_service import get_connection
import services.reservation_service as reservation_service

# verifico che la funzione reserve_book gestisca correttamente due casi: il libro è inesistente e prenotazione riuscita
@pytest.mark.parametrize(
    "available_copies, rowcount, expected_success, expected_msg",
    [
        (None, 0, False, "Libro non trovato."),
        (2,    1, True,  "Prenotazione confermata"),
    ],
)

def test_reserve_book(mocker, available_copies, rowcount, expected_success, expected_msg):
    fake_conn = mocker.MagicMock()
    mocker.patch("services.reservation_service.get_connection") \
          .return_value.__enter__.return_value = fake_conn

    select_result = mocker.MagicMock()
    select_result.fetchone.return_value = (
        None if available_copies is None
        else {"available_copies": available_copies, "title": "Titolo"}
    )

    update_cursor = mocker.MagicMock()
    update_cursor.rowcount = rowcount

    fake_conn.execute.side_effect = [select_result, update_cursor, mocker.MagicMock()]

    success, message = reservation_service.reserve_book(user_id=1, book_id=42)

    assert success == expected_success
    assert expected_msg in message


# verifico che la funzione cancel_reservation gestisca correttamente la cancellazione di una prenotazione
@pytest.mark.parametrize(
    "row, expected_success, expected_msg",
    [
        (None, False, "Prenotazione non trovata."),
        ({"id": 1, "book_id": 10, "status": "active"}, True, "Prenotazione cancellata"),
    ],
)

def test_cancel_reservation(mocker, row, expected_success, expected_msg):
    fake_conn = mocker.MagicMock()
    mocker.patch("services.reservation_service.get_connection") \
          .return_value.__enter__.return_value = fake_conn

    select_result = mocker.MagicMock()
    select_result.fetchone.return_value = row

    fake_conn.execute.side_effect = [select_result, mocker.MagicMock(), mocker.MagicMock()]

    success, message = reservation_service.cancel_reservation(1, 1)

    assert success == expected_success
    assert expected_msg in message


# verifico che la funzione get_user_reservations restituisca correttamente la lista delle prenotazioni di un utente
def test_get_user_reservations(mocker):
    fake_conn = mocker.MagicMock()
    mocker.patch("services.reservation_service.get_connection") \
          .return_value.__enter__.return_value = fake_conn

    fake_conn.execute.return_value.fetchall.return_value = [
        {
            "id": 1, "user_id": 1, "book_id": 10,
            "reserved_at": "2025-01-01", "status": "active",
            "book_title": "Python", "book_author": "Guido",
        }
    ]

    result = reservation_service.get_user_reservations(1)

    assert len(result) == 1
    assert result[0].id == 1
    assert result[0].book_title == "Python"