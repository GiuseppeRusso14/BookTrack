import pytest

from cli.app import _main_menu, run


@pytest.fixture
def user(mocker):
    u = mocker.MagicMock()
    u.full_name = "Mario Rossi"
    return u


def test_choice_1_browse_catalog(mocker, user):
    mock_browse = mocker.patch("cli.app.browse_catalog")
    mocker.patch("builtins.input", return_value="1")

    result = _main_menu(user)

    assert result is True
    mock_browse.assert_called_once()


def test_choice_2_search_books(mocker, user):
    mock_search = mocker.patch("cli.app.search_books_menu")
    mocker.patch("builtins.input", return_value="2")

    result = _main_menu(user)

    assert result is True
    mock_search.assert_called_once()


def test_choice_3_reserve_book(mocker, user):
    mock_reserve = mocker.patch("cli.app.reserve_book_menu")
    mocker.patch("builtins.input", return_value="3")

    result = _main_menu(user)

    assert result is True
    mock_reserve.assert_called_once_with(user)


def test_choice_4_my_reservations(mocker, user):
    mock_my = mocker.patch("cli.app.my_reservations_menu")
    mocker.patch("builtins.input", return_value="4")

    result = _main_menu(user)

    assert result is True
    mock_my.assert_called_once_with(user)


def test_choice_5_logout(mocker, user, capsys):
    mocker.patch("builtins.input", return_value="5")

    result = _main_menu(user)

    assert result is False
    assert "Arrivederci" in capsys.readouterr().out


def test_invalid_choice(mocker, user, capsys):
    mocker.patch("builtins.input", return_value="9")

    result = _main_menu(user)

    assert result is True
    assert "non valida" in capsys.readouterr().out


def test_run_user_exits_immediately(mocker, capsys):
    mocker.patch("cli.app.login_screen", return_value=None)

    run()

    assert "Chiusura" in capsys.readouterr().out


def test_run_login_then_logout(mocker, user):
    mock_login = mocker.patch("cli.app.login_screen", side_effect=[user, None])
    mocker.patch("builtins.input", return_value="5")

    run()

    assert mock_login.call_count == 2
