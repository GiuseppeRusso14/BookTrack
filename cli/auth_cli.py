from typing import Optional

from models.user import User
from services import auth_service


def login_screen() -> Optional[User]:
    print("\n" + "=" * 50)
    print("       BOOKSHELF - Accesso")
    print("=" * 50)

    usernames = auth_service.get_all_usernames()
    print("\nUtenti disponibili:")
    for u in usernames:
        print(f"  - {u}")

    print("\nInserisci le credenziali (o 'esci' per chiudere).")

    while True:
        username = input("Username: ").strip()
        if username.lower() == "esci":
            return None
        password = input("Password: ").strip()

        user = auth_service.authenticate(username, password)
        if user is not None:
            print(f"\nBenvenuto/a, {user.full_name}!")
            return user
        print("\nCredenziali non valide. Riprova.\n")
