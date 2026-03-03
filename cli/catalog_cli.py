from services import book_service

def browse_catalog() -> None:
    books = book_service.get_all_books()
    print("\n" + "=" * 70)
    print("  CATALOGO LIBRI")
    print("=" * 70)
    if not books:
        print("  Nessun libro presente nel catalogo.")
        return
    for book in books:
        print(f"  {book}")
    print(f"\n  Totale: {len(books)} titoli")


def search_books_menu() -> None:
    query = input("\nCerca per titolo, autore o genere: ").strip()
    if not query:
        print("Ricerca annullata.")
        return
    results = book_service.search_books(query)
    if not results:
        print(f"Nessun risultato per '{query}'.")
        return
    print(f"\n  Risultati per '{query}' ({len(results)}):")
    for book in results:
        print(f"  {book}")