# 📚 BookTrack

**Sistema di gestione e prenotazione libri con controllo delle disponibilità.**

BookShelf è un'applicazione CLI sviluppata in Python che consente agli utenti di consultare un catalogo di libri, verificarne la disponibilità e procedere con la prenotazione. Al momento della prenotazione, il numero di copie disponibili viene automaticamente decrementato per garantire la coerenza dei dati.

## Caratteristiche principali

- Catalogo iniziale composto da circa una ventina di titoli precaricati
- Prenotazione libri con decremento automatico delle copie disponibili
- Autenticazione tramite un insieme di utenti predefiniti, con corretta progettazione delle entità e delle relazioni tra di esse
- Persistenza dei dati tra un'esecuzione e l'altra tramite database locale SQLite
- Architettura modulare con separazione tra logica applicativa e gestione dell'interfaccia, predisposta per una futura estensione come web app

## Nota sull'autenticazione

L'implementazione di un sistema completo di registrazione con gestione sicura delle password richiederebbe componenti che esulano dagli obiettivi attuali del project work. Per questo motivo si è scelto di utilizzare un insieme di utenti predefiniti, garantendo comunque una corretta progettazione delle entità e delle relazioni tra di esse.

## Stack tecnologico

- **Linguaggio:** Python
- **Database:** SQLite
- **Interfaccia:** CLI (Command Line Interface)