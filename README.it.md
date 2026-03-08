# 📚 BookTrack
![Lint](https://github.com/GiuseppeRusso14/BookTrack/actions/workflows/lint.yml/badge.svg)
![Test](https://github.com/GiuseppeRusso14/BookTrack/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/GiuseppeRusso14/BookTrack/branch/main/graph/badge.svg)](https://codecov.io/gh/GiuseppeRusso14/BookTrack)

🇮🇹 Leggi in italiano | 🇬🇧 [Read in English](README.md)

**BookTrack** è un'applicazione **a riga di comando (CLI)** sviluppata in Python che permette agli utenti di esplorare un catalogo di libri, controllare quante copie sono disponibili, prenotare libri e cancellare prenotazioni attive.

Il database SQLite viene **generato all'avvio** dell'applicazione e i record iniziali sono **precaricati dal file `seed.py` nella cartella `db`**, garantendo la coerenza dei dati tra un utilizzo e l'altro. L'applicazione ha un'**architettura modulare** 🌐, pensata per facilitare una futura estensione come **web app**. I principali servizi sono testati con **pytest** ✅ e ogni modifica viene verificata automaticamente tramite la **pipeline CI/CD**, assicurando che le funzionalità restino corrette.



## Funzionalità principali

- Catalogo di circa **20 titoli precaricati** con titolo, autore e genere.
- **Verifica disponibilità** delle copie prima di prenotare.
- **Prenotazione libri** con decremento automatico delle copie disponibili.
- **Cancellazione prenotazioni** attive, con ripristino delle copie.
- **Visualizzazione prenotazioni** dell'utente con dettagli su libro, data e stato.
- **Autenticazione utenti** tramite insieme di utenti predefiniti.



## Architettura e gestione dati

- **Persistenza dei dati** tramite database locale SQLite.
- **Architettura modulare**: separazione tra logica applicativa e interfaccia.
- **Test automatizzati** delle funzioni principali con pytest, per garantire correttezza e coerenza dei dati.



## Struttura del progetto

```
booktrack/
├── db/              # Inizializzazione e connessione al database
├── models/          # Definizione delle entità (Book, User, Reservation)
├── services/        # Logica applicativa
├── cli/             # Interfaccia a riga di comando
├── tests/           # Test unitari sviluppati usando pytest
└── main.py          # Entry point dell'applicazione
```



## Strumenti e framework

- **Python 3.12**
- **SQLite** per il database
- **pytest** per i test
- **pytest-mock** per il mocking delle connessioni e delle query
- **GitHub Actions** per la pipeline CI/CD: lint e test automatici ad ogni PR, con **coverage minimo del 75%**



## Avvio rapido

```bash
# Clona il repository
git clone https://github.com/<username>/booktrack.git
cd booktrack

# (Consigliato) Crea e attiva un ambiente virtuale
python3 -m venv venv
source venv/bin/activate  # Su Windows: venv\Scripts\activate

# Installa le dipendenze
pip install -r requirements.txt

# Esegui l'applicazione
python3 main.py
```



## Note sul linguaggio

L'interfaccia CLI è in **italiano**, perché l'applicazione è destinata a un pubblico italofono. Il codice interno, le funzioni e i nomi delle variabili sono scritti in **inglese**, seguendo le convenzioni standard dello sviluppo software.



## Nota sull'autenticazione

L'implementazione di un sistema completo di registrazione con gestione sicura delle password richiederebbe componenti che esulano dagli obiettivi attuali del project work. Per questo motivo si è scelto di utilizzare un insieme di utenti predefiniti, garantendo comunque una corretta progettazione delle entità e delle relazioni tra di esse.



## Credenziali di accesso

L'applicazione include cinque utenti predefiniti:

| Username        | Password    | Nome completo  |
|-----------------|-------------|----------------|
| `mario_rossi`   | `password1` | Mario Rossi    |
| `laura_bianchi` | `password2` | Laura Bianchi  |
| `luca_verdi`    | `password3` | Luca Verdi     |
| `anna_neri`     | `password4` | Anna Neri      |
| `paolo_gialli`  | `password5` | Paolo Gialli   |
