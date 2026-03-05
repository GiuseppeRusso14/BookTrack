from .catalog_cli import browse_catalog, search_books_menu

def _main_menu():
    print("\n" + "-" * 40)
    print(f"  Menu principale")
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
        # prenota un libro
        pass
    elif choice == "4":
        # visualizza prenotazioni utente
        pass
    elif choice == "5":
        print(f"\n  Arrivederci!")
        return False
    else:
        print("  Scelta non valida.")
    return True

def run():
    running = True
    while running:
        running = _main_menu()