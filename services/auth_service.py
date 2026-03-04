from typing import List, Optional

from db.connection import get_connection
from models.user import User


def authenticate(username: str, password: str) -> Optional[User]:
    conn = get_connection()
    row = conn.execute(
        "SELECT id, username, password, full_name FROM users "
        "WHERE username = ? AND password = ?",
        (username, password),
    ).fetchone()
    if row is None:
        return None
    return User(
        id=row["id"],
        username=row["username"],
        password=row["password"],
        full_name=row["full_name"],
    )


def get_all_usernames() -> List[str]:
    conn = get_connection()
    rows = conn.execute("SELECT username FROM users ORDER BY username").fetchall()
    return [row["username"] for row in rows]
