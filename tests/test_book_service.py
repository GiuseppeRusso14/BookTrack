from services.book_service import _row_to_book, get_all_books, get_available_books, get_book_by_id, search_books

# Verifico che una riga del database venga trasformata correttamente in un oggetto Book
def test_row_to_book():
    row = {
        "id": 1,
        "title": "Python",
        "author": "Guido",
        "genre": "Programming",
        "year": 1991,
        "total_copies": 5,
        "available_copies": 3
    }

    book = _row_to_book(row)

    assert book.id == 1
    assert book.title == "Python"
    assert book.author == "Guido"
    assert book.genre == "Programming"
    assert book.year == 1991
    assert book.total_copies == 5
    assert book.available_copies == 3


# Verifico che la funzione restituisca tutti i libri presenti nel catalogo
def test_get_all_books(mocker):

    fake_rows = [
        {
            "id": 1,
            "title": "Python",
            "author": "Guido",
            "genre": "Programming",
            "year": 1991,
            "total_copies": 5,
            "available_copies": 3,
        }
    ]

    mock_conn = mocker.Mock()
    mock_conn.execute.return_value.fetchall.return_value = fake_rows

    mock_get_connection = mocker.patch("services.book_service.get_connection")
    mock_get_connection.return_value.__enter__.return_value = mock_conn

    books = get_all_books()

    assert len(books) == 1
    assert books[0].title == "Python"

# Verifico che la funzione restituisca solo libri con copie disponibili
def test_get_available_books(mocker):

    fake_rows = [
        {
            "id": 1,
            "title": "Python",
            "author": "Guido",
            "genre": "Programming",
            "year": 1991,
            "total_copies": 5,
            "available_copies": 2,
        }
    ]

    mock_conn = mocker.Mock()
    mock_conn.execute.return_value.fetchall.return_value = fake_rows

    mock_get_connection = mocker.patch("services.book_service.get_connection")
    mock_get_connection.return_value.__enter__.return_value = mock_conn

    books = get_available_books()

    assert books[0].available_copies > 0
    
# Verifico che la funzione restituisca il libro corretto dato un id esistente
def test_get_book_by_id_found(mocker):

    fake_row = {
        "id": 1,
        "title": "Python",
        "author": "Guido",
        "genre": "Programming",
        "year": 1991,
        "total_copies": 5,
        "available_copies": 3,
    }

    mock_conn = mocker.Mock()
    mock_conn.execute.return_value.fetchone.return_value = fake_row

    mock_get_connection = mocker.patch("services.book_service.get_connection")
    mock_get_connection.return_value.__enter__.return_value = mock_conn

    book = get_book_by_id(1)

    assert book.title == "Python"

# Verifico che la funzione restituisca None se il libro con l'id specificato non esiste
def test_get_book_by_id_not_found(mocker):

    mock_conn = mocker.Mock()
    mock_conn.execute.return_value.fetchone.return_value = None

    mock_get_connection = mocker.patch("services.book_service.get_connection")
    mock_get_connection.return_value.__enter__.return_value = mock_conn

    book = get_book_by_id(999)

    assert book is None


# Verifico che la funzione restituisca i libri che corrispondono alla ricerca
def test_search_books(mocker):

    fake_rows = [
        {
            "id": 1,
            "title": "Python Basics",
            "author": "Guido",
            "genre": "Programming",
            "year": 1991,
            "total_copies": 5,
            "available_copies": 3,
        }
    ]

    mock_conn = mocker.Mock()
    mock_conn.execute.return_value.fetchall.return_value = fake_rows

    mock_get_connection = mocker.patch("services.book_service.get_connection")
    mock_get_connection.return_value.__enter__.return_value = mock_conn

    books = search_books("Python")

    assert len(books) == 1
    assert books[0].title == "Python Basics"