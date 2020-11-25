from __future__ import annotations

from flask import Flask

from config import Config


__version__ = "0.0.4"


app = Flask(__name__)
app.config.from_object(Config)


from app import routes  # noqa: E402


_ = routes
