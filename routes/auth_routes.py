#!/usr/bin/python3
"""
Module contains the blueprint for the authentication routes of the application.

The blueprint contains the following routes:
    - /login: for logging in to the application
    - /logout: for logging out of the application
    - /register: for registering a new user account

The blueprint also contains the following functions:
    - init_login_manager: for initializing the login manager
    - load_user: for loading the user from the database based on their ID
    - logout: for logging out the user and clearing the session
    - login: for handling the login form submission
    - register: for handling the registration form submission
"""

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
    """
    Function as helper method that initializes both the login manager for the application
    and bcrypt for hashing user password.

    Parameters:
        app (Flask): The Flask application.
    """
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"
    login_manager.session_protection = "strong"
    bcrypt.init_app(app)


# region load user from db
@login_manager.user_loader
def load_user(user_id):
    """
    Function as helper method that loads the user from the database based on their ID.

    Parameters:
        user_id (std): The ID as UUID of the user to be loaded.

    Returns:
        A User object that corresponds to the user with the given ID or None if no user
        with the given ID is found.
    """
    return User.query.get(user_id)

# endregion load user from db


# region Logout
@auth_bp.route("/logout")
@login_required
def logout():
    """
    Function that logs out the current logged in user and clears the session.

    Returns:
        A redirect to the landing page of the application.
    """
    logout_user()
    session.clear()
    response = make_response(redirect(url_for("main_bp.landing_page")))
    response.delete_cookie("session")
    return response


# endregion Logout


# region Login
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Function that Login user to the application.
    
    Args:
        form (LoginForm): The login form.

    Returns:
        A redirect to the user's profile page if login is successful,
        or a template with the login form if login is unsuccessful.
    """
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
    """
    Function that register a new user to the application.

    Args:
        form (LoginForm): The login form.

    Returns:
        A redirect to the login page if registration is successful,
        or a template with the register form if unsuccessful.
    """
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            username=form.username.data,
            gender=form.gender.data,
            password=bcrypt.generate_password_hash(form.password.data)
        )
        new_user.save()
        return redirect(url_for("auth_bp.login"))

    return render_template("register.html", form=form)


# endregion signup
