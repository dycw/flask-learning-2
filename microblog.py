from __future__ import annotations

from typing import Any
from typing import Dict

from app import app
from app import db
from app.models import Post
from app.models import User


@app.shell_context_processor
def make_shell_context() -> Dict[str, Any]:
    return {"db": db, "User": User, "Post": Post}
