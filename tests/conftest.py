import pytest
import db.connection as db_conn

@pytest.fixture(autouse=True)
def reset_db_singleton():
    if db_conn._connection is not None:
        db_conn._connection.close()
        db_conn._connection = None
    yield
    if db_conn._connection is not None:
        db_conn._connection.close()
        db_conn._connection = None
