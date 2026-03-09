from typing import List, Tuple

from db.connection import get_connection
from models.reservation import Reservation


def reserve_book(user_id: int, book_id: int) -> Tuple[bool, str]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT available_copies, title FROM books WHERE id = ?", (book_id,)
        ).fetchone()
        if row is None:
            return False, "Libro non trovato."
        if row["available_copies"] <= 0:
            return False, f"'{row['title']}' non ha copie disponibili."

        cursor = conn.execute(
            "UPDATE books SET available_copies = available_copies - 1 "
            "WHERE id = ? AND available_copies > 0",
            (book_id,),
        )
        if cursor.rowcount == 0:
            return False, "Nessuna copia disponibile."

        conn.execute(
            "INSERT INTO reservations (user_id, book_id) VALUES (?, ?)",
            (user_id, book_id),
        )
        conn.commit()
        return True, f"Prenotazione confermata per '{row['title']}'."


def cancel_reservation(reservation_id: int, user_id: int) -> Tuple[bool, str]:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, book_id, status FROM reservations WHERE id = ? AND user_id = ?",
            (reservation_id, user_id),
        ).fetchone()

        if row is None:
            return False, "Prenotazione non trovata."

        if row["status"] != "active":
            return False, "La prenotazione è già stata cancellata."

        conn.execute(
            "UPDATE reservations SET status = 'cancelled' WHERE id = ?",
            (reservation_id,),
        )

        conn.execute(
            "UPDATE books SET available_copies = available_copies + 1 WHERE id = ?",
            (row["book_id"],),
        )

        conn.commit()

    return True, "Prenotazione cancellata. La copia è di nuovo disponibile."


def get_user_reservations(user_id: int) -> List[Reservation]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT r.id, r.user_id, r.book_id, r.reserved_at, r.status, "
            "b.title AS book_title, b.author AS book_author "
            "FROM reservations r "
            "JOIN books b ON r.book_id = b.id "
            "WHERE r.user_id = ? "
            "ORDER BY r.reserved_at DESC",
            (user_id,),
        ).fetchall()

    return [
        Reservation(
            id=r["id"],
            user_id=r["user_id"],
            book_id=r["book_id"],
            reserved_at=r["reserved_at"],
            status=r["status"],
            book_title=r["book_title"],
            book_author=r["book_author"],
        )
        for r in rows
    ]
