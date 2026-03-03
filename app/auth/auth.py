from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app.extension import db
from app.model import User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        if not username or not password or not email:
            flash("All fields required")
            return redirect(url_for("auth.register"))

        if User.query.filter_by(username=username).first():
            flash("Username already taken")
            return redirect(url_for("auth.register"))

        new_user = User(username, password, email)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if not user or not user.password_check(password):
            flash("Invalid credentials")
            return redirect(url_for("auth.login"))

        login_user(user)
        return redirect(url_for("main.index"))

    return render_template("login.html")


@auth_bp.route("/logout/")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
