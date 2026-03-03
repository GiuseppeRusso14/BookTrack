from db.seed import initialize_database
from db.connection import close_connection
#from cli.app import run

def main():
    try:
        initialize_database()
        #run()
    except KeyboardInterrupt:
        print("\n\n  Applicazione interrotta. A presto!")
    finally:
        close_connection()


if __name__ == "__main__":
    main()