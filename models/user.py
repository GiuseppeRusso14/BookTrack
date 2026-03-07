from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password: str
    full_name: str

    def __str__(self) -> str:
        return f"{self.full_name} (@{self.username})"
