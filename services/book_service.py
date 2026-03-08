from typing import List, Optional

from db.connection import get_connection
from models.book import Book


def _row_to_book(row) -> Book:
    return Book(
        id=row["id"],
        title=row["title"],
        author=row["author"],
        genre=row["genre"],
        year=row["year"],
        total_copies=row["total_copies"],
        available_copies=row["available_copies"],
    )


def get_all_books() -> List[Book]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM books ORDER BY title").fetchall()
        return [_row_to_book(r) for r in rows]


def get_available_books() -> List[Book]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM books WHERE available_copies > 0 ORDER BY title"
        ).fetchall()
        return [_row_to_book(r) for r in rows]


def get_book_by_id(book_id: int) -> Optional[Book]:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
        if row is None:
            return None
        return _row_to_book(row)


def search_books(query: str) -> List[Book]:
    like = f"%{query}%"
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT * FROM books "
            "WHERE title LIKE ? OR author LIKE ? OR genre LIKE ? "
            "ORDER BY title",
            (like, like, like),
        ).fetchall()
        return [_row_to_book(r) for r in rows]
