from .connection import get_connection

def initialize_database() -> None:
    conn = get_connection()
    _create_tables(conn)
    conn.commit()


def _create_tables(conn) -> None:
    conn.executescript(
        """
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
    """
    )