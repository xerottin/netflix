# tests/test_auth.py
from app.auth import authenticate_user
from app.models import Users


def test_authenticate_user_success(db):
    user = authenticate_user("testuser", "testpassword", db)
    assert user is not None
    assert user.username == "testuser"


def test_authenticate_user_wrong_password(db):
    user = authenticate_user("testuser", "wrongpassword", db)
    assert user is None


def test_authenticate_user_nonexistent_user(db):
    user = authenticate_user("nonexistent", "testpassword", db)
    assert user is None
