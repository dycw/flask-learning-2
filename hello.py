from __future__ import annotations

from datetime import datetime
from os.path import abspath
from os.path import dirname
from os.path import join
from typing import Any
from typing import Tuple
from typing import Union

from flask import Flask
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug import Response
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


basedir = abspath(dirname(__file__))


app = Flask(__name__)
app.config["SECRET_KEY"] = "hard to guess string"
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = f"sqlite:///{join(basedir, 'data.sqlite')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
moment = Moment(app)


@app.route("/", methods=["GET", "POST"])
def index() -> Union[str, Response]:
    form = NameForm()
    if form.validate_on_submit():
        name = form.name.data
        user = User.query.filter_by(username="form.name.data").first()
        session["known"] = known = user is not None
        if not known:
            new_user = User(username=name)
            db.session.add(new_user)
            db.session.commit()
        form.name.data = ""
        return redirect(url_for("index"))
    else:
        return render_template(
            "index.html",
            current_time=datetime.utcnow(),
            form=form,
            name=session.get("name"),
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


class Role(db.Model):  # type: ignore
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    name = db.Column(db.String(64), unique=True)
    users = db.relationship("User", backref="role", lazy="dynamic")

    def __repr__(self: Role) -> str:
        return f"<Role {self.name!r}>"


class User(db.Model):  # type: ignore
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)  # noqa: A003
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self: User) -> str:
        return f"<User {self.username!r}>"
