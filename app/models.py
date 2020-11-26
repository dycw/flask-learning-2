from __future__ import annotations

from datetime import datetime
from hashlib import md5
from typing import Callable
from typing import cast

from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app import db
from app import login
from utilities import T


class User(UserMixin, db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self: User) -> str:
        return f"<User {self.username}>"

    def avatar(self: User, size: int) -> str:
        digest = md5(  # noqa: S303
            self.email.lower().encode("utf-8"),
        ).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"

    def set_password(self: User, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self: User, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Post(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self: Post) -> str:
        return f"<Post {self.body}>"


@cast(Callable[[T], T], login.user_loader)
def load_user(id: str) -> User:  # noqa: A002
    return User.query.get(int(id))
