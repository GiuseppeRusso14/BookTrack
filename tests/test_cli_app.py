from unittest.mock import patch

from cli import app


def test_main_menu_choice_1_returns_true():
    with patch("builtins.input", return_value="1"):
        result = app._main_menu()
    assert result is True


def test_main_menu_choice_2_returns_true():
    with patch("builtins.input", return_value="2"):
        result = app._main_menu()
    assert result is True


def test_main_menu_choice_3_returns_true():
    with patch("builtins.input", return_value="3"):
        result = app._main_menu()
    assert result is True


def test_main_menu_choice_4_returns_true():
    with patch("builtins.input", return_value="4"):
        result = app._main_menu()
    assert result is True


def test_main_menu_choice_5_returns_false():
    with patch("builtins.input", return_value="5"):
        result = app._main_menu()
    assert result is False


def test_main_menu_invalid_choice_returns_true():
    with patch("builtins.input", return_value="9"):
        result = app._main_menu()
    assert result is True


def test_main_menu_empty_choice_returns_true():
    with patch("builtins.input", return_value=""):
        result = app._main_menu()
    assert result is True


def test_main_menu_prints_options(capsys):
    with patch("builtins.input", return_value="5"):
        app._main_menu()
    captured = capsys.readouterr()
    assert "Sfoglia catalogo" in captured.out
    assert "Logout" in captured.out
