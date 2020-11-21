from __future__ import annotations

from typing import Any
from typing import Tuple

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/user/<name>")
def user(name: str) -> str:
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found(e: Any) -> Tuple[str, int]:  # noqa: U100
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e: Any) -> Tuple[str, int]:  # noqa: U100
    return render_template("500.html"), 500
