import pytest

from cli.reservation_cli import my_reservations_menu, reserve_book_menu
from models.user import User

FAKE_USER = User(id=1, username="giuseppe", password="hash", full_name="Giuseppe Russo")


@pytest.fixture
def mock_book(mocker):
    book = mocker.Mock()
    book.is_available = True
    book.title = "Dune"
    book.__str__ = mocker.Mock(return_value="[1] Dune - Frank Herbert")
    return book


@pytest.fixture
def mock_reservation(mocker):
    res = mocker.Mock()
    res.is_active = True
    return res


# --- reserve_book_menu ---


def test_no_books_available(mocker, capsys):
    mocker.patch(
        "cli.reservation_cli.book_service.get_available_books", return_value=[]
    )

    reserve_book_menu(FAKE_USER)

    assert "Nessun libro disponibile" in capsys.readouterr().out


def test_invalid_input(mocker, capsys, mock_book):
    mocker.patch(
        "cli.reservation_cli.book_service.get_available_books", return_value=[mock_book]
    )
    mocker.patch("builtins.input", return_value="abc")

    reserve_book_menu(FAKE_USER)

    assert "Input non valido" in capsys.readouterr().out


def test_user_cancels_with_zero(mocker, mock_book):
    mocker.patch(
        "cli.reservation_cli.book_service.get_available_books", return_value=[mock_book]
    )
    mocker.patch("builtins.input", return_value="0")
    mock_reserve = mocker.patch("cli.reservation_cli.reservation_service.reserve_book")

    reserve_book_menu(FAKE_USER)

    mock_reserve.assert_not_called()


def test_book_not_found(mocker, capsys, mock_book):
    mocker.patch(
        "cli.reservation_cli.book_service.get_available_books", return_value=[mock_book]
    )
    mocker.patch("cli.reservation_cli.book_service.get_book_by_id", return_value=None)
    mocker.patch("builtins.input", return_value="99")

    reserve_book_menu(FAKE_USER)

    assert "Libro non disponibile" in capsys.readouterr().out


def test_book_not_available(mocker, capsys, mock_book):
    mock_book.is_available = False
    mocker.patch(
        "cli.reservation_cli.book_service.get_available_books", return_value=[mock_book]
    )
    mocker.patch(
        "cli.reservation_cli.book_service.get_book_by_id", return_value=mock_book
    )
    mocker.patch("builtins.input", return_value="1")

    reserve_book_menu(FAKE_USER)

    assert "Libro non disponibile" in capsys.readouterr().out


def test_user_declines_confirmation(mocker, capsys, mock_book):
    mocker.patch(
        "cli.reservation_cli.book_service.get_available_books", return_value=[mock_book]
    )
    mocker.patch(
        "cli.reservation_cli.book_service.get_book_by_id", return_value=mock_book
    )
    mocker.patch("builtins.input", side_effect=["1", "n"])
    mock_reserve = mocker.patch("cli.reservation_cli.reservation_service.reserve_book")

    reserve_book_menu(FAKE_USER)

    mock_reserve.assert_not_called()
    assert "annullata" in capsys.readouterr().out


def test_reservation_success(mocker, capsys, mock_book):
    mocker.patch(
        "cli.reservation_cli.book_service.get_available_books", return_value=[mock_book]
    )
    mocker.patch(
        "cli.reservation_cli.book_service.get_book_by_id", return_value=mock_book
    )
    mocker.patch(
        "cli.reservation_cli.reservation_service.reserve_book",
        return_value=(True, "Prenotazione confermata"),
    )
    mocker.patch("builtins.input", side_effect=["1", "s"])

    reserve_book_menu(FAKE_USER)

    assert "Prenotazione confermata" in capsys.readouterr().out


# --- my_reservations_menu ---


def test_no_reservations(mocker, capsys):
    mocker.patch(
        "cli.reservation_cli.reservation_service.get_user_reservations", return_value=[]
    )

    my_reservations_menu(FAKE_USER)

    assert "Non hai prenotazioni" in capsys.readouterr().out


def test_all_reservations_inactive(mocker, mock_reservation):
    mock_reservation.is_active = False
    mocker.patch(
        "cli.reservation_cli.reservation_service.get_user_reservations",
        return_value=[mock_reservation],
    )
    mock_input = mocker.patch("builtins.input")

    my_reservations_menu(FAKE_USER)

    mock_input.assert_not_called()


def test_user_enters_zero_to_go_back(mocker, mock_reservation):
    mocker.patch(
        "cli.reservation_cli.reservation_service.get_user_reservations",
        return_value=[mock_reservation],
    )
    mocker.patch("builtins.input", return_value="0")
    mock_cancel = mocker.patch(
        "cli.reservation_cli.reservation_service.cancel_reservation"
    )

    my_reservations_menu(FAKE_USER)

    mock_cancel.assert_not_called()


def test_invalid_cancel_input(mocker, mock_reservation):
    mocker.patch(
        "cli.reservation_cli.reservation_service.get_user_reservations",
        return_value=[mock_reservation],
    )
    mocker.patch("builtins.input", return_value="abc")
    mock_cancel = mocker.patch(
        "cli.reservation_cli.reservation_service.cancel_reservation"
    )

    my_reservations_menu(FAKE_USER)

    mock_cancel.assert_not_called()


def test_cancellation_success(mocker, capsys, mock_reservation):
    mocker.patch(
        "cli.reservation_cli.reservation_service.get_user_reservations",
        return_value=[mock_reservation],
    )
    mocker.patch(
        "cli.reservation_cli.reservation_service.cancel_reservation",
        return_value=(True, "Prenotazione cancellata"),
    )
    mocker.patch("builtins.input", return_value="1")

    my_reservations_menu(FAKE_USER)

    assert "Prenotazione cancellata" in capsys.readouterr().out
