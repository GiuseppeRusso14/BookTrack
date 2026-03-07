from cli.auth_cli import login_screen
from cli.catalog_cli import browse_catalog, search_books_menu
from models.user import User

def _main_menu(user: User) -> bool:
    print("\n" + "-" * 40)
    print(f"  Menu principale  |  {user.full_name}")
    print("-" * 40)
    print("  1. Sfoglia catalogo")
    print("  2. Cerca libri")
    print("  3. Prenota un libro")
    print("  4. Le mie prenotazioni")
    print("  5. Logout")
    print("-" * 40)

    choice = input("  Scelta: ").strip()

    if choice == "1":
        browse_catalog()
    elif choice == "2":
        search_books_menu()
    elif choice == "3":
        pass
    elif choice == "4":
        pass
    elif choice == "5":
        print(f"\n  Arrivederci, {user.full_name}!")
        return False
    else:
        print("  Scelta non valida.")
    return True

def run() -> None:
    print("\n" + "=" * 50)
    print("     BOOKSHELF - Gestione e Prenotazione Libri")
    print("=" * 50)

    while True:
        user = login_screen()
        if user is None:
            print("\n  Chiusura dell'applicazione. A presto!")
            break
        while _main_menu(user):
            pass