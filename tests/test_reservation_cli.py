import pytest
from models.user import User
from cli.reservation_cli import reserve_book_menu, my_reservations_menu


FAKE_USER = User(id=1, username="giuseppe", password="hash", full_name="Giuseppe Russo")


# --- reserve_book_menu ---

# Verifico che la funzione stampi un messaggio e esca se non ci sono libri disponibili
def test_reserve_book_menu_no_books(mocker, capsys):
    mocker.patch("cli.reservation_cli.book_service.get_available_books", return_value=[])

    reserve_book_menu(FAKE_USER)

    captured = capsys.readouterr()
    assert "Nessun libro disponibile" in captured.out


# Verifico che la funzione gestisca un input non numerico senza crashare
def test_reserve_book_menu_invalid_input(mocker, capsys):
    fake_book = mocker.Mock()
    fake_book.__str__ = mocker.Mock(return_value="[1] Python - Guido")
    mocker.patch("cli.reservation_cli.book_service.get_available_books", return_value=[fake_book])
    mocker.patch("builtins.input", return_value="abc")

    reserve_book_menu(FAKE_USER)

    captured = capsys.readouterr()
    assert "Input non valido" in captured.out


# Verifico che la funzione esca senza prenotare se l'utente inserisce 0
def test_reserve_book_menu_cancel_with_zero(mocker):
    fake_book = mocker.Mock()
    mocker.patch("cli.reservation_cli.book_service.get_available_books", return_value=[fake_book])
    mocker.patch("builtins.input", return_value="0")
    mock_reserve = mocker.patch("cli.reservation_cli.reservation_service.reserve_book")

    reserve_book_menu(FAKE_USER)

    mock_reserve.assert_not_called()


# Verifico che la funzione stampi un errore se il libro non esiste
def test_reserve_book_menu_book_not_found(mocker, capsys):
    fake_book = mocker.Mock()
    mocker.patch("cli.reservation_cli.book_service.get_available_books", return_value=[fake_book])
    mocker.patch("builtins.input", return_value="99")
    mocker.patch("cli.reservation_cli.book_service.get_book_by_id", return_value=None)

    reserve_book_menu(FAKE_USER)

    captured = capsys.readouterr()
    assert "Libro non disponibile" in captured.out


# Verifico che la funzione stampi un errore se il libro non è disponibile
def test_reserve_book_menu_book_not_available(mocker, capsys):
    fake_book = mocker.Mock()
    fake_book.is_available = False
    mocker.patch("cli.reservation_cli.book_service.get_available_books", return_value=[fake_book])
    mocker.patch("builtins.input", return_value="1")
    mocker.patch("cli.reservation_cli.book_service.get_book_by_id", return_value=fake_book)

    reserve_book_menu(FAKE_USER)

    captured = capsys.readouterr()
    assert "Libro non disponibile" in captured.out


# Verifico che la funzione esca senza prenotare se l'utente non conferma
def test_reserve_book_menu_user_does_not_confirm(mocker, capsys):
    fake_book = mocker.Mock()
    fake_book.is_available = True
    fake_book.title = "Python"
    mocker.patch("cli.reservation_cli.book_service.get_available_books", return_value=[fake_book])
    mocker.patch("cli.reservation_cli.book_service.get_book_by_id", return_value=fake_book)
    mocker.patch("builtins.input", side_effect=["1", "n"])
    mock_reserve = mocker.patch("cli.reservation_cli.reservation_service.reserve_book")

    reserve_book_menu(FAKE_USER)

    mock_reserve.assert_not_called()
    captured = capsys.readouterr()
    assert "annullata" in captured.out


# Verifico che la funzione chiami reserve_book e stampi il messaggio di conferma
def test_reserve_book_menu_success(mocker, capsys):
    fake_book = mocker.Mock()
    fake_book.is_available = True
    fake_book.title = "Python"
    mocker.patch("cli.reservation_cli.book_service.get_available_books", return_value=[fake_book])
    mocker.patch("cli.reservation_cli.book_service.get_book_by_id", return_value=fake_book)
    mocker.patch("builtins.input", side_effect=["1", "s"])
    mocker.patch(
        "cli.reservation_cli.reservation_service.reserve_book",
        return_value=(True, "Prenotazione confermata"),
    )

    reserve_book_menu(FAKE_USER)

    captured = capsys.readouterr()
    assert "Prenotazione confermata" in captured.out


# --- my_reservations_menu ---

# Verifico che la funzione stampi un messaggio se l'utente non ha prenotazioni
def test_my_reservations_menu_no_reservations(mocker, capsys):
    mocker.patch("cli.reservation_cli.reservation_service.get_user_reservations", return_value=[])

    my_reservations_menu(FAKE_USER)

    captured = capsys.readouterr()
    assert "Non hai prenotazioni" in captured.out


# Verifico che la funzione non chieda la cancellazione se non ci sono prenotazioni attive
def test_my_reservations_menu_no_active_reservations(mocker):
    fake_res = mocker.Mock()
    fake_res.is_active = False
    mocker.patch(
        "cli.reservation_cli.reservation_service.get_user_reservations",
        return_value=[fake_res],
    )
    mock_input = mocker.patch("builtins.input")

    my_reservations_menu(FAKE_USER)

    mock_input.assert_not_called()


# Verifico che la funzione esca senza cancellare se l'utente inserisce 0
def test_my_reservations_menu_cancel_with_zero(mocker):
    fake_res = mocker.Mock()
    fake_res.is_active = True
    mocker.patch(
        "cli.reservation_cli.reservation_service.get_user_reservations",
        return_value=[fake_res],
    )
    mocker.patch("builtins.input", return_value="0")
    mock_cancel = mocker.patch("cli.reservation_cli.reservation_service.cancel_reservation")

    my_reservations_menu(FAKE_USER)

    mock_cancel.assert_not_called()


# Verifico che la funzione esca senza cancellare se l'utente inserisce un valore non numerico
def test_my_reservations_menu_invalid_cancel_input(mocker):
    fake_res = mocker.Mock()
    fake_res.is_active = True
    mocker.patch(
        "cli.reservation_cli.reservation_service.get_user_reservations",
        return_value=[fake_res],
    )
    mocker.patch("builtins.input", return_value="abc")
    mock_cancel = mocker.patch("cli.reservation_cli.reservation_service.cancel_reservation")

    my_reservations_menu(FAKE_USER)

    mock_cancel.assert_not_called()


# Verifico che la funzione chiami cancel_reservation e stampi il messaggio di risposta
def test_my_reservations_menu_cancel_success(mocker, capsys):
    fake_res = mocker.Mock()
    fake_res.is_active = True
    mocker.patch(
        "cli.reservation_cli.reservation_service.get_user_reservations",
        return_value=[fake_res],
    )
    mocker.patch("builtins.input", return_value="1")
    mocker.patch(
        "cli.reservation_cli.reservation_service.cancel_reservation",
        return_value=(True, "Prenotazione cancellata"),
    )

    my_reservations_menu(FAKE_USER)

    captured = capsys.readouterr()
    assert "Prenotazione cancellata" in captured.out
