from __future__ import annotations

from flask import Flask


__version__ = "0.0.3"


app = Flask(__name__)


from app import routes  # noqa: E402


_ = routes
