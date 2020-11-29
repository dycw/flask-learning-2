from __future__ import annotations

from sqlalchemy.orm import scoped_session

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


def test_follow(db_session: scoped_session) -> None:
    u1 = User(username="john", email="john@example.com")
    u2 = User(username="susan", email="susan@example.com")
    db_session.add(u1)
    db_session.add(u2)
    db_session.commit()
    assert u1.followed.all() == []
    assert u1.followers.all() == []
    u1.follow(u2)
    db_session.commit()
    assert u1.is_following(u2)
    assert u1.followed.count() == 1
    assert u1.followed.first().username == "susan"
    assert u2.followers.count() == 1
    assert u2.followers.first().username == "john"
    u1.unfollow(u2)
    db_session.commit()
    assert not u1.is_following(u2)
    assert u1.followed.count() == 0
    assert u2.followers.count() == 0
