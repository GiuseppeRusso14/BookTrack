import pytest

from cli.auth_cli import login_screen


@pytest.fixture(autouse=True)
def mock_usernames(mocker):
    mocker.patch(
        "cli.auth_cli.auth_service.get_all_usernames", return_value=["mario", "luigi"]
    )


def test_user_types_exit(mocker, capsys):
    mocker.patch("builtins.input", return_value="esci")

    result = login_screen()

    assert result is None


def test_login_success(mocker, capsys):
    fake_user = mocker.MagicMock()
    fake_user.full_name = "Mario Rossi"

    mocker.patch("cli.auth_cli.auth_service.authenticate", return_value=fake_user)
    mocker.patch("builtins.input", side_effect=["mario", "password123"])

    result = login_screen()

    assert result == fake_user
    assert "Benvenuto/a, Mario Rossi" in capsys.readouterr().out


def test_invalid_credentials_then_exit(mocker, capsys):
    mocker.patch("cli.auth_cli.auth_service.authenticate", return_value=None)
    mocker.patch("builtins.input", side_effect=["mario", "sbagliata", "esci"])

    result = login_screen()

    assert result is None
    assert "Credenziali non valide" in capsys.readouterr().out


def test_wrong_credentials_twice_then_login(mocker, capsys):
    fake_user = mocker.MagicMock()
    fake_user.full_name = "Luigi Verdi"

    mocker.patch(
        "cli.auth_cli.auth_service.authenticate", side_effect=[None, None, fake_user]
    )
    mocker.patch("builtins.input", side_effect=["x", "x", "x", "x", "luigi", "giusta"])

    result = login_screen()

    assert result == fake_user


def test_available_users_are_displayed(mocker, capsys):
    mocker.patch("builtins.input", return_value="esci")

    login_screen()

    output = capsys.readouterr().out
    assert "mario" in output
    assert "luigi" in output
