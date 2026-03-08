# 📚 BookTrack
![Lint](https://github.com/GiuseppeRusso14/BookTrack/actions/workflows/lint.yml/badge.svg)
![Test](https://github.com/GiuseppeRusso14/BookTrack/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/GiuseppeRusso14/BookTrack/branch/main/graph/badge.svg)](https://codecov.io/gh/GiuseppeRusso14/BookTrack)

🇮🇹 [Leggi in italiano](README.it.md) | 🇬🇧 Read in English

**BookTrack** is a **command-line (CLI) application** built in Python that allows users to browse a book catalog, check copy availability, reserve books, and cancel active reservations.

The SQLite database is **generated at startup** and pre-populated with initial records from `seed.py` in the `db` folder, ensuring data consistency across sessions. The application follows a **modular architecture** 🌐 designed to facilitate a future extension as a **web app**. Core services are tested with **pytest** ✅ and every change is automatically verified through the **CI/CD pipeline**, ensuring features remain correct.



## Features

- Catalog of approximately **20 pre-loaded titles** with title, author, and genre.
- **Availability check** before reserving a book.
- **Book reservation** with automatic decrement of available copies.
- **Cancellation of active reservations**, restoring the copy count.
- **Reservation overview** with details on book, date, and status.
- **User authentication** via a set of predefined users.



## Architecture & Data Management

- **Data persistence** via a local SQLite database.
- **Modular architecture**: clear separation between business logic and interface.
- **Automated tests** for core functions with pytest, ensuring correctness and data consistency.



## Project Structure

```
booktrack/
├── db/              # Database initialization and connection
├── models/          # Entity definitions (Book, User, Reservation)
├── services/        # Business logic
├── cli/             # Command-line interface
├── tests/           # Unit tests built with pytest
└── main.py          # Application entry point
```



## Tools & Frameworks

- **Python 3.12**
- **SQLite** for the database
- **pytest** for testing
- **pytest-mock** for mocking connections and queries
- **GitHub Actions** for the CI/CD pipeline: automated lint and tests on every PR, with a **minimum coverage of 75%**



## Quick Start

```bash
# Clone the repository
git clone https://github.com/<username>/booktrack.git
cd booktrack

# (Recommended) Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python3 main.py
```



## Language Notes

The CLI interface is presented in **Italian**, as the application is intended for an Italian-speaking audience. Internal code, functions, and variable names are written in **English** following standard development conventions.



## Note on Authentication

Implementing a full registration system with secure password management would require components that go beyond the current scope of this project. For this reason, a set of predefined users has been used, while still ensuring a proper design of the entities and their relationships.



## Login Credentials

The application includes five predefined users:

| Username        | Password    | Full Name      |
|-----------------|-------------|----------------|
| `mario_rossi`   | `password1` | Mario Rossi    |
| `laura_bianchi` | `password2` | Laura Bianchi  |
| `luca_verdi`    | `password3` | Luca Verdi     |
| `anna_neri`     | `password4` | Anna Neri      |
| `paolo_gialli`  | `password5` | Paolo Gialli   |