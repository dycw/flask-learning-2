from __future__ import annotations

from flask import render_template

from app import app


@app.route("/")
@app.route("/index")
def index() -> str:
    user = {"username": "Miguel"}
    return render_template("index.html", title="Home", user=user)
