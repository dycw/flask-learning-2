from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Tuple

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.route("/", methods=["GET", "POST"])
def index() -> str:
    name = None
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ""
    return render_template(
        "index.html",
        current_time=datetime.utcnow(),
        form=form,
        name=name,
    )


@app.route("/user/<name>")
def user(name: str) -> str:
    return render_template("user.html", name=name)


@app.errorhandler(404)
def page_not_found(e: Any) -> Tuple[str, int]:  # noqa: U100
    return render_template("404.html"), 404


@app.errorhandler(500)
def internal_server_error(e: Any) -> Tuple[str, int]:  # noqa: U100
    return render_template("500.html"), 500


class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")
