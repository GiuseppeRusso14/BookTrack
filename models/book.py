from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    author: str
    genre: str
    year: int
    total_copies: int
    available_copies: int

    @property
    def is_available(self) -> bool:
        return self.avalaible_copies>0

    def __str__(self) -> str:
        status=f"{self.available_copies}/{self.total_copies} disponibili"
        return f"[{self.id}] {self.title} - {self.author} ({self.year}) | {self.genre} | {status}"