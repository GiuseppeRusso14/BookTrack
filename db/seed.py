from db.connection import get_connection


def initialize_database() -> None:
    conn = get_connection()
    _create_tables(conn)
    _seed_users(conn)
    _seed_books(conn)
    conn.commit()


def _create_tables(conn) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            username  TEXT    NOT NULL UNIQUE,
            password  TEXT    NOT NULL,
            full_name TEXT    NOT NULL
        );

        CREATE TABLE IF NOT EXISTS books (
            id               INTEGER PRIMARY KEY AUTOINCREMENT,
            title            TEXT    NOT NULL,
            author           TEXT    NOT NULL,
            genre            TEXT    NOT NULL,
            year             INTEGER NOT NULL,
            total_copies     INTEGER NOT NULL DEFAULT 3,
            available_copies INTEGER NOT NULL DEFAULT 3
        );

        CREATE TABLE IF NOT EXISTS reservations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id     INTEGER NOT NULL,
            book_id     INTEGER NOT NULL,
            reserved_at TEXT    NOT NULL DEFAULT (datetime('now', 'localtime')),
            status      TEXT    NOT NULL DEFAULT 'active',
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (book_id) REFERENCES books(id)
        );
    """)


def _seed_users(conn) -> None:
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    if count > 0:
        return
    users = [
        ("mario_rossi", "password1", "Mario Rossi"),
        ("laura_bianchi", "password2", "Laura Bianchi"),
        ("luca_verdi", "password3", "Luca Verdi"),
        ("anna_neri", "password4", "Anna Neri"),
        ("paolo_gialli", "password5", "Paolo Gialli"),
    ]
    conn.executemany(
        "INSERT INTO users (username, password, full_name) VALUES (?, ?, ?)",
        users,
    )


def _seed_books(conn) -> None:
    count = conn.execute("SELECT COUNT(*) FROM books").fetchone()[0]
    if count > 0:
        return
    books = [
        ("Il nome della rosa", "Umberto Eco", "Romanzo storico", 1980, 3, 3),
        ("1984", "George Orwell", "Distopia", 1949, 3, 3),
        ("Il piccolo principe", "Antoine de Saint-Exupéry", "Narrativa", 1943, 5, 5),
        ("Orgoglio e pregiudizio", "Jane Austen", "Romanzo", 1813, 3, 3),
        ("Il Signore degli Anelli", "J.R.R. Tolkien", "Fantasy", 1954, 4, 4),
        (
            "Cent'anni di solitudine",
            "Gabriel García Márquez",
            "Realismo magico",
            1967,
            3,
            3,
        ),
        ("Il processo", "Franz Kafka", "Narrativa", 1925, 2, 2),
        ("Don Chisciotte", "Miguel de Cervantes", "Romanzo", 1605, 2, 2),
        ("La divina commedia", "Dante Alighieri", "Poesia epica", 1320, 4, 4),
        ("I promessi sposi", "Alessandro Manzoni", "Romanzo storico", 1827, 3, 3),
        ("Harry Potter e la pietra filosofale", "J.K. Rowling", "Fantasy", 1997, 5, 5),
        ("Il vecchio e il mare", "Ernest Hemingway", "Narrativa", 1952, 3, 3),
        ("Fahrenheit 451", "Ray Bradbury", "Fantascienza", 1953, 3, 3),
        ("Il grande Gatsby", "F. Scott Fitzgerald", "Romanzo", 1925, 3, 3),
        ("Moby Dick", "Herman Melville", "Avventura", 1851, 2, 2),
        ("Anna Karenina", "Lev Tolstoj", "Romanzo", 1877, 3, 3),
        ("Il giorno della civetta", "Leonardo Sciascia", "Giallo", 1961, 3, 3),
        ("Se questo è un uomo", "Primo Levi", "Memorialistica", 1947, 4, 4),
        ("Il barone rampante", "Italo Calvino", "Romanzo", 1957, 3, 3),
        ("La coscienza di Zeno", "Italo Svevo", "Romanzo", 1923, 2, 2),
    ]
    conn.executemany(
        "INSERT INTO books (title, author, genre, year, total_copies, available_copies) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        books,
    )
