from models.user import User
from services import book_service, reservation_service


def reserve_book_menu(user: User) -> None:
    books = book_service.get_available_books()
    if not books:
        print("\nNessun libro disponibile per la prenotazione.")
        return

    print("\n  LIBRI DISPONIBILI:")
    for book in books:
        print(f"  {book}")

    try:
        book_id = int(
            input("\nInserisci l'ID del libro da prenotare (0 per annullare): ")
        )
    except ValueError:
        print("Input non valido.")
        return
    if book_id == 0:
        return

    book = book_service.get_book_by_id(book_id)
    if book is None or not book.is_available:
        print("Libro non disponibile.")
        return

    confirm = (
        input(f"Confermi la prenotazione di '{book.title}'? (s/n): ").strip().lower()
    )
    if confirm != "s":
        print("Prenotazione annullata.")
        return

    success, message = reservation_service.reserve_book(user.id, book_id)
    print(f"\n  {message}")


def my_reservations_menu(user: User) -> None:
    reservations = reservation_service.get_user_reservations(user.id)
    if not reservations:
        print("\n  Non hai prenotazioni.")
        return

    print("\n  LE TUE PRENOTAZIONI:")
    active_count = 0
    for r in reservations:
        print(f"  {r}")
        if r.is_active:
            active_count += 1

    if active_count == 0:
        return

    cancel = input(
        "\nVuoi cancellare una prenotazione? Inserisci l'ID (0 per tornare): "
    ).strip()
    try:
        cancel_id = int(cancel)
    except ValueError:
        return
    if cancel_id == 0:
        return

    success, message = reservation_service.cancel_reservation(cancel_id, user.id)
    print(f"\n  {message}")
