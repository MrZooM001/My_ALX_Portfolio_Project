#!/usr/bin/python3
from flask_restx import Namespace, Resource
from flask import jsonify, request, make_response
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt_identity,
                                jwt_required)
from flask_restx import Resource, fields
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_namespace = Namespace(
    "Authentication", description="Namespace for authentication."
)


signup_model = auth_namespace.model(
    "SignUp",
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
    },
)

login_model = auth_namespace.model(
    "Login", {"username": fields.String(), "password": fields.String()}
)


# region Login using JWT
@auth_namespace.route("/signup")
class Signup(Resource):
    """
    Class that represents the signup process.

    Methods:
        post -- creates a new user and save it to the database
    """

    @auth_namespace.expect(signup_model)
    def post(self):
        data = request.get_json()

        username = data.get("username")

        # Check if the user already exists in the database
        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify(
                {
                    "message": "User with username {} already exists"
                    .format(username)
                }
            )

        # Create a new user's signup instance
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=generate_password_hash(data.get("password"))
        )

        new_user.save()
        return jsonify({"message": "User created successfully"})


# endregion Login using JWT


# region Login using JWT
@auth_namespace.route("/login")
class Login(Resource):
    """
    Class that represents the login process
    and handle the JWT authentication.

    Methods:
        post -- creates a new login session.
    """

    @auth_namespace.expect(login_model)
    def post(self):
        # handle data coming from clients as json
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            if check_password_hash(db_user.password, password):
                access_tok = create_access_token(identity=db_user.username)
                refresh_tok = create_refresh_token(identity=db_user.username)
            else:
                return jsonify({"message": "Invalid password"})

            return jsonify({"access_token": access_tok, "refresh_token": refresh_tok})
        else:
            return jsonify({"message": "Username does not exist"})


# endregion Login using JWT


@auth_namespace.route('/refresh')
class RefreshToken(Resource):
    """Class that represents refresh access token"""
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_tok = create_access_token(identity=current_user)

        return make_response(jsonify({"message": new_access_tok}), 200)
