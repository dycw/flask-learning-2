from __future__ import annotations

from os import environ
from pathlib import Path


basedir = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = (
        environ.get(
            "DATABASE_URL",
        )
        or "sqlite:///{}".format(basedir.joinpath("app.db"))
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = environ.get("MAIL_SERVER") or "smtp.googlemail.com"
    MAIL_PORT = int(environ.get("MAIL_PORT") or 587)
    MAIL_USE_TLS = environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = environ.get("MAIL_USERNAME") or "derek.wan.test2@gmail.com"
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD") or "lewis wet sucks luke"
    ADMINS = ["d.wan@icloud.com"]
