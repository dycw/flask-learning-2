from __future__ import annotations

from app import db


class User(db.Model):  # type: ignore
    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self: User) -> str:
        return f"<User {self.username}>"
