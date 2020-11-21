from __future__ import annotations

from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route("/")
def index() -> str:
    return render_template("index.html")


@app.route("/user/<name>")
def user(name: str) -> str:
    return render_template("user.html", name=name)
