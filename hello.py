from __future__ import annotations

from flask import Flask
from flask import request


app = Flask(__name__)


@app.route("/")
def index() -> str:
    user_agent = request.headers.get("User-Agent")
    return f"<p>Your browser is {user_agent}</p>"


@app.route("/user/<name>")
def user(name: str) -> str:
    return f"<h1>Hello, {name}!</h1>"
