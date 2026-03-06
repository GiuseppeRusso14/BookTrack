from typing import Tuple
from db.connection import get_connection

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