from models.user import User


def test_user_str():
    user = User(id=1, username="mario", password="secret", full_name="Mario Rossi")
    assert str(user) == "Mario Rossi (@mario)"