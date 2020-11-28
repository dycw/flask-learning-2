from __future__ import annotations

from app.models import User


def test_password_hashing() -> None:
    u = User(username="susan")
    u.set_password("cat")
    assert not u.check_password("dog")
    assert u.check_password("cat")


def test_avatar() -> None:
    u = User(username="john", email="john@example.com")
    assert u.avatar(128) == (
        "https://www.gravatar.com/avatar/"
        "d4c74594d841139328695756648b6bd6?d=identicon&s=128"
    )
