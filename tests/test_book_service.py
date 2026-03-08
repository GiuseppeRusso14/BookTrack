import pytest
from services.book_service import _row_to_book, get_all_books, get_available_books, get_book_by_id, search_books

@pytest.fixture
def fake_book_row():
    return {
        "id": 1,
        "title": "Python",
        "author": "Guido",
        "genre": "Programming",
        "year": 1991,
        "total_copies": 5,
        "available_copies": 3,
    }

@pytest.fixture
def fake_conn(mocker):
    mock_conn = mocker.Mock()
    mocker.patch("services.book_service.get_connection") \
          .return_value.__enter__.return_value = mock_conn
    return mock_conn

def test_row_to_book(fake_book_row):
    book = _row_to_book(fake_book_row)
    assert book.id == 1
    assert book.title == "Python"
    assert book.author == "Guido"
    assert book.genre == "Programming"
    assert book.year == 1991
    assert book.total_copies == 5
    assert book.available_copies == 3

def test_get_all_books(fake_conn, fake_book_row):
    fake_conn.execute.return_value.fetchall.return_value = [fake_book_row]
    books = get_all_books()
    assert len(books) == 1
    assert books[0].title == "Python"
    assert books[0].author == "Guido"

def test_get_all_books_empty(fake_conn):
    fake_conn.execute.return_value.fetchall.return_value = []
    books = get_all_books()
    assert books == []

def test_get_available_books(fake_conn, fake_book_row):
    fake_conn.execute.return_value.fetchall.return_value = [fake_book_row]
    books = get_available_books()
    assert len(books) == 1
    assert books[0].available_copies > 0

def test_get_available_books_empty(fake_conn):
    fake_conn.execute.return_value.fetchall.return_value = []
    books = get_available_books()
    assert books == []

def test_get_book_by_id_found(fake_conn, fake_book_row):
    fake_conn.execute.return_value.fetchone.return_value = fake_book_row
    book = get_book_by_id(1)
    assert book.id == 1
    assert book.title == "Python"
    assert book.author == "Guido"

def test_get_book_by_id_not_found(fake_conn):
    fake_conn.execute.return_value.fetchone.return_value = None
    book = get_book_by_id(999)
    assert book is None

def test_search_books(fake_conn, fake_book_row):
    search_row = {**fake_book_row, "title": "Python Basics"}
    fake_conn.execute.return_value.fetchall.return_value = [search_row]
    books = search_books("Python")
    assert len(books) == 1
    assert books[0].title == "Python Basics"

def test_search_books_no_results(fake_conn):
    fake_conn.execute.return_value.fetchall.return_value = []
    books = search_books("XYZ non esiste")
    assert books == []

def test_book_is_available_true(fake_book_row):
    book = _row_to_book(fake_book_row)
    assert book.is_available is True

def test_book_is_available_false(fake_book_row):
    fake_book_row["available_copies"] = 0
    book = _row_to_book(fake_book_row)
    assert book.is_available is False

def test_book_str(fake_book_row):
    book = _row_to_book(fake_book_row)
    result = str(book)
    assert "Python" in result
    assert "Guido" in result
    assert "3/5 disponibili" in result