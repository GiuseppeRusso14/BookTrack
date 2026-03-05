from unittest.mock import patch

from models.user import User
from cli import auth_cli


def _mock_user():
    return User(id=1, username="mario", password="pass1", full_name="Mario Rossi")


def test_login_screen_success():
    user = _mock_user()
    with patch("cli.auth_cli.auth_service.get_all_usernames", return_value=["mario", "laura"]):
        with patch("cli.auth_cli.auth_service.authenticate", return_value=user):
            with patch("builtins.input", side_effect=["mario", "pass1"]):
                result = auth_cli.login_screen()
    assert result is user


def test_login_screen_esci():
    with patch("cli.auth_cli.auth_service.get_all_usernames", return_value=["mario"]):
        with patch("builtins.input", return_value="esci"):
            result = auth_cli.login_screen()
    assert result is None


def test_login_screen_esci_case_insensitive():
    with patch("cli.auth_cli.auth_service.get_all_usernames", return_value=["mario"]):
        with patch("builtins.input", return_value="ESCI"):
            result = auth_cli.login_screen()
    assert result is None


def test_login_screen_retry_then_success():
    user = _mock_user()
    with patch("cli.auth_cli.auth_service.get_all_usernames", return_value=["mario"]):
        with patch(
            "cli.auth_cli.auth_service.authenticate", side_effect=[None, user]
        ):
            with patch(
                "builtins.input", side_effect=["mario", "wrong", "mario", "pass1"]
            ):
                result = auth_cli.login_screen()
    assert result is user


def test_login_screen_shows_usernames(capsys):
    user = _mock_user()
    with patch("cli.auth_cli.auth_service.get_all_usernames", return_value=["mario", "laura"]):
        with patch("cli.auth_cli.auth_service.authenticate", return_value=user):
            with patch("builtins.input", side_effect=["mario", "pass1"]):
                auth_cli.login_screen()
    captured = capsys.readouterr()
    assert "mario" in captured.out
    assert "laura" in captured.out
