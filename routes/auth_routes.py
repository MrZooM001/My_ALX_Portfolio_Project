#!/usr/bin/python3
from flask import Blueprint, make_response, render_template, url_for, redirect, session
from flask_login import login_user, login_required, logout_user
from forms import LoginForm, RegisterForm
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models import User



auth_bp = Blueprint('auth_bp', __name__)

login_manager = LoginManager()
bcrypt = Bcrypt()


def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"
    login_manager.session_protection = "strong"
    bcrypt.init_app(app)


# region load user from db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# endregion load user from db


# region Logout
@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    response = make_response(redirect(url_for("main_bp.landing_page")))
    response.delete_cookie("session")
    return response


# endregion Logout


# region Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("main_bp.profile"))

    return render_template("login.html", form=form)


# endregion Login


# region signup
@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            username=form.username.data,
            password=bcrypt.generate_password_hash(form.password.data),
        )
        new_user.save()
        return redirect(url_for("auth_bp.login"))

    return render_template("register.html", form=form)


# endregion signup
