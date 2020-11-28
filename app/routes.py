from __future__ import annotations

from typing import Callable
from typing import cast
from typing import Union

from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from IPython.utils.tz import utcnow
from werkzeug import Response
from werkzeug.urls import url_parse

from app import app
from app import db
from app.forms import EditProfileForm
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User
from utilities import T


@app.route("/")
@app.route("/index")
@cast(Callable[[T], T], login_required)
def index() -> str:
    posts = [
        {
            "author": {"username": "John"},
            "body": "Beautiful day in Portland!",
        },
        {
            "author": {"username": "Susan"},
            "body": "The Avengers movie was so cool!",
        },
    ]
    return render_template(
        "index.html",
        title="Home",
        posts=posts,
    )


@app.route("/login", methods=["GET", "POST"])
def login() -> Union[str, Response]:
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if (user is None) or not user.check_password(form.password.data):
                flash("Invalid username or password")
                return redirect(url_for("login"))
            else:
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get("next")
                if (not next_page) or (url_parse(next_page).netloc != ""):
                    return redirect(url_for("index"))
                else:
                    return redirect(next_page)
        else:
            return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout() -> Response:
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register() -> Union[str, Response]:
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    else:
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Congratulations, you are now a registered user!")
            return redirect(url_for("login"))
        else:
            return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@cast(Callable[[T], T], login_required)
def user(username: str) -> str:
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {"author": user, "body": "Test post #1"},
        {"author": user, "body": "Test post #2"},
    ]
    return render_template("user.html", user=user, posts=posts)


@app.before_request
def before_request() -> None:
    if current_user.is_authenticated:
        current_user.last_seen = utcnow()
        db.session.commit()


@app.route("/edit_profile", methods=["GET", "POST"])
@cast(Callable[[T], T], login_required)
def edit_profile() -> Union[str, Response]:
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    else:
        if request.method == "GET":
            form.username.data = current_user.username
            form.about_me.data = current_user.about_me
        return render_template(
            "edit_profile.html",
            title="Edit Profile",
            form=form,
        )
