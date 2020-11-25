from __future__ import annotations

from typing import Union

from flask import flash
from flask import redirect
from flask import render_template
from werkzeug import Response

from app import app
from app.forms import LoginForm


@app.route("/")
@app.route("/index")
def index() -> str:
    user = {"username": "Miguel"}
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
        user=user,
        posts=posts,
    )


@app.route("/login", methods=["GET", "POST"])
def login() -> Union[str, Response]:
    form = LoginForm()
    if form.validate_on_submit():
        flash(
            f"Login requested for user {form.username.data},"
            f"remember_me={form.remember_me.data}",
        )
        return redirect("/index")
    else:
        return render_template("login.html", title="Sign In", form=form)
