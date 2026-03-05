from models.user import User


def test_user_str():
    user = User(id=1, username="mario", password="pass", full_name="Mario Rossi")
    assert str(user) == "Mario Rossi (@mario)"


def test_user_fields():
    user = User(id=2, username="laura", password="secret", full_name="Laura Bianchi")
    assert user.id == 2
    assert user.username == "laura"
    assert user.password == "secret"
    assert user.full_name == "Laura Bianchi"


def test_user_equality():
    u1 = User(id=1, username="mario", password="pass", full_name="Mario Rossi")
    u2 = User(id=1, username="mario", password="pass", full_name="Mario Rossi")
    assert u1 == u2


def test_user_different():
    u1 = User(id=1, username="mario", password="pass", full_name="Mario Rossi")
    u2 = User(id=2, username="laura", password="pass2", full_name="Laura Bianchi")
    assert u1 != u2
