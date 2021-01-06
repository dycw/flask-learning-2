from __future__ import annotations

from logging import ERROR
from logging import Formatter
from logging import INFO
from logging.handlers import RotatingFileHandler
from logging.handlers import SMTPHandler
from pathlib import Path
from typing import Optional
from typing import Tuple

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config


__version__ = "0.0.10"


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"


if not app.debug:
    if app.config["MAIL_SERVER"]:
        if app.config["MAIL_USERNAME"] or app.config["MAIL_PASSWORD"]:
            auth: Optional[Tuple[str, str]] = (
                app.config["MAIL_USERNAME"],
                app.config["MAIL_PASSWORD"],
            )
        else:
            auth = None
        if app.config["MAIL_USE_TLS"]:
            secure: Optional[Tuple] = ()
        else:
            secure = None
        mail_handler = SMTPHandler(
            mailhost=(app.config["MAIL_SERVER"], app.config["MAIL_PORT"]),
            fromaddr="no-reply@" + app.config["MAIL_SERVER"],
            toaddrs=app.config["ADMINS"],
            subject="Microblog Failure",
            credentials=auth,
            secure=secure,  # type: ignore
        )
        mail_handler.setLevel(ERROR)
        app.logger.addHandler(mail_handler)

    if not (path := Path("logs")).exists():
        path.mkdir()
    file_handler = RotatingFileHandler(
        "logs/microblog.log",
        maxBytes=10240,
        backupCount=10,
    )
    file_handler.setFormatter(
        Formatter(
            "%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]",
        ),
    )
    file_handler.setLevel(INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(INFO)
    app.logger.info("Microblog startup")


from app import models  # noqa:E402
from app import routes  # noqa:E402
from app import errors  # noqa:E402


_ = (errors, models, routes)
