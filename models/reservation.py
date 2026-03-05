from dataclasses import dataclass

@dataclass
class Reservation:
    id: int
    user_id: int
    book_id: int
    reserved_at: str
    status: str
    book_title: str = ""
    book_author: str = ""

    @property
    def is_active(self) -> bool:
        return self.status == "active"

    def __str__(self) -> str:
        stato = "Attiva" if self.is_active else "Cancellata"
        return f"[{self.id}] {self.book_title} di {self.book_author} | {self.reserved_at} | {stato}"
