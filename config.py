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
