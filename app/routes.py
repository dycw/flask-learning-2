from __future__ import annotations

from app import app


@app.route("/")
@app.route("/index")
def index() -> str:
    return "Hello, World!"
