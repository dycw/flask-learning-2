from __future__ import annotations

from app.models import User


def test_password_hashing() -> None:
    u = User(username="susan")
    u.set_password("cat")
    assert not u.check_password("dog")
    assert u.check_password("cat")
