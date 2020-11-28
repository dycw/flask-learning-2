from __future__ import annotations

import os
from os import environ
from pathlib import Path


basedir = Path(__file__).resolve().parent


class Config:
    SECRET_KEY = environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get(
            "DATABASE_URL",
        )
        or "sqlite:///{}".format(basedir.joinpath("app.db"))
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT") or 25)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS") is not None
    MAIL_USERNAME = (
        os.environ.get("MAIL_USERNAME") or "derek.wan.test2@gmail.com"
    )
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD") or "lewis wet sucks luke"
    ADMINS = ["d.wan@icloud.com"]
