from __future__ import annotations

from datetime import datetime
from hashlib import md5
from typing import Callable
from typing import cast

from flask_login import UserMixin
from flask_sqlalchemy import BaseQuery
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import db
from app import login
from utilities import T


followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("user.id")),
)


class User(UserMixin, db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # noqa:A003
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        "User",
        secondary=followers,
        primaryjoin=followers.c.follower_id == id,
        secondaryjoin=followers.c.followed_id == id,
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )

    def avatar(self: User, size: int) -> str:
        digest = md5(  # noqa:DUO130,S303
            self.email.lower().encode("utf-8"),
        ).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def set_password(self: User, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self: User, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def follow(self: User, user: User) -> None:
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self: User, user: User) -> None:
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self: User, user: User) -> bool:
        return (
            self.followed.filter(
                followers.c.followed_id == user.id,
            ).count()
            > 0
        )

    def followed_posts(self: User) -> BaseQuery:
        followed = (
            Post.query.join(
                followers,
                followers.c.followed_id == Post.user_id,
            )
            .filter(followers.c.follower_id == self.id)
            .order_by(Post.timestamp.desc())
        )
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())

    def __repr__(self: User) -> str:
        return f"<User {self.username}>"


class Post(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # noqa:A003
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self: Post) -> str:
        return f"<Post {self.body}>"


@cast(Callable[[T], T], login.user_loader)
def load_user(id: str) -> User:  # noqa:A002
    return User.query.get(int(id))
