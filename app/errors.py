from __future__ import annotations

from typing import Tuple

from flask import render_template
from werkzeug.exceptions import NotFound

from app import app
from app import db


@app.errorhandler(404)
def not_found_error(error: NotFound) -> Tuple[str, int]:  # noqa: U100
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_error(error: int) -> Tuple[str, int]:
    raise TypeError(type(error))
    db.session.rollback()
    return render_template("500.html"), 500
