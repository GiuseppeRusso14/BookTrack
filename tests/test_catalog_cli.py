import pytest
from cli import catalog_cli
from models.book import Book

@pytest.fixture
def fake_book():
    return Book(
        id=1,
        title="Python",
        author="Guido",
        genre="Programming",
        year=1991,
        total_copies=5,
        available_copies=3,
    )

@pytest.fixture
def mock_book_service(mocker, fake_book):
    mocker.patch("cli.catalog_cli.book_service.get_all_books", return_value=[fake_book])
    mocker.patch("cli.catalog_cli.book_service.search_books", return_value=[fake_book])
    return mocker

def test_browse_catalog_with_books(mock_book_service, capsys):
    catalog_cli.browse_catalog()
    captured = capsys.readouterr()
    assert "CATALOGO LIBRI" in captured.out
    assert "Python" in captured.out
    assert "Totale: 1 titoli" in captured.out

def test_browse_catalog_empty(mocker, capsys):
    mocker.patch("cli.catalog_cli.book_service.get_all_books", return_value=[])
    catalog_cli.browse_catalog()
    captured = capsys.readouterr()
    assert "Nessun libro presente nel catalogo." in captured.out

def test_search_books_menu_with_results(mocker, fake_book, capsys):
    mocker.patch("builtins.input", return_value="Python")
    mocker.patch("cli.catalog_cli.book_service.search_books", return_value=[fake_book])
    catalog_cli.search_books_menu()
    captured = capsys.readouterr()
    assert "Risultati per 'Python'" in captured.out
    assert "Python" in captured.out

def test_search_books_menu_no_results(mocker, capsys):
    mocker.patch("builtins.input", return_value="XYZ")
    mocker.patch("cli.catalog_cli.book_service.search_books", return_value=[])
    catalog_cli.search_books_menu()
    captured = capsys.readouterr()
    assert "Nessun risultato per 'XYZ'." in captured.out

def test_search_books_menu_empty_query(mocker, capsys):
    mocker.patch("builtins.input", return_value="")
    catalog_cli.search_books_menu()
    captured = capsys.readouterr()
    assert "Ricerca annullata." in captured.out