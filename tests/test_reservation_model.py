import pytest

from models.reservation import Reservation


@pytest.fixture
def active_reservation():
    return Reservation(
        id=1,
        user_id=1,
        book_id=10,
        reserved_at="2025-01-01",
        status="active",
        book_title="Python",
        book_author="Guido",
    )


@pytest.fixture
def cancelled_reservation():
    return Reservation(
        id=2,
        user_id=1,
        book_id=10,
        reserved_at="2025-01-01",
        status="cancelled",
        book_title="Python",
        book_author="Guido",
    )


def test_is_active_true(active_reservation):
    assert active_reservation.is_active is True


def test_is_active_false(cancelled_reservation):
    assert cancelled_reservation.is_active is False


def test_reservation_str_active(active_reservation):
    result = str(active_reservation)
    assert "Python" in result
    assert "Guido" in result
    assert "Attiva" in result


def test_reservation_str_cancelled(cancelled_reservation):
    result = str(cancelled_reservation)
    assert "Cancellata" in result
