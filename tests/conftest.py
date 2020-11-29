from __future__ import annotations

from typing import Any
from typing import Callable
from typing import cast

from _pytest.fixtures import SubRequest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from pytest import fixture

from app import db
from utilities import T


@cast(Callable[[T], T], fixture(scope="session"))
def database(request: SubRequest) -> None:
    db.create_all()

    @cast(Callable[[T], T], request.addfinalizer)
    def drop_database() -> None:
        db.drop_all()


@cast(Callable[[T], T], fixture(scope="session"))
def app(database: Any) -> Flask:  # noqa: U100
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
    return app


@cast(Callable[[T], T], fixture(scope="session"))
def _db(app: Flask) -> SQLAlchemy:
    return SQLAlchemy(app=app)
