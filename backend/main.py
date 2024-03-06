#!/usr/bin/env python3
""" Module to configure flask application """

from config import DevConfig
from extentions import db
from flask import Flask, jsonify, request
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    create_refresh_token,
    jwt_required
)
from flask_migrate import Migrate
from flask_restx import Api, Resource, fields
from models import Recipe, User
from werkzeug.security import generate_password_hash, check_password_hash


# region app intialization
app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
migrate = Migrate(app, db)
JWTManager(app)

api = Api(app, doc="/docs")

recipe_model = api.model(
    "Recipe",
    {
        "id": fields.String(),
        "title": fields.String(),
        "description": fields.String()
    }
)

signup_model = api.model(
    "SignUp",
    {
        "username": fields.String(),
        "email": fields.String(),
        "password": fields.String(),
    }
)

login_model = api.model(
    "Login",
    {
        "username": fields.String(),
        "password": fields.String()
    }
)


# endregion app intialization


# region Flask interactive shell
@app.shell_context_processor
def make_shell_context():
    """
    makes application objects available in the Python Flask interactive shell

    Examples:
    >>> flask shell
    or
    >>> flask db init
    """
    return {"db": db, "Recipe": Recipe}


# endregion Flask interactive shell


# region Hello World
@api.route("/hello")
class Helo(Resource):
    def get(self):
        """
        Return a simple test message in JSON format.

        Returns:
            JSON object containing the greeting message
        """
        return {"message": "Hello World!"}


# endregion Hello World


# region Signup / Login using JWT
@api.route("/signup")
class Signup(Resource):
    """
    Class that represents the signup process.

    Methods:
        post -- creates a new user and save it to the database
    """

    @api.expect(signup_model)
    def post(self):
        data = request.get_json()

        username = data.get("username")

        # Check if the user already exists in the database
        db_user = User.query.filter_by(username=username).first()
        if db_user is not None:
            return jsonify(
                {"message": "User with username {} already exists"
                 .format(username)})

        # Create a new user's signup instance
        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password=generate_password_hash(data.get("password"))
        )

        new_user.save()
        return jsonify({"message": "User created successfully"})


@api.route("/login")
class Login(Resource):
    """
    Class that represents the login process
    and handle the JWT authentication.

    Methods:
        post -- creates a new login session.
    """

    @api.expect(login_model)
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

            return jsonify(
                {"access_token": access_tok,
                 "refresh_token": refresh_tok})
        else:
            return jsonify({"message": "Username does not exist"})


# endregion Signup / Login using JWT


# region All Recipes
@api.route("/recipes")
class RecipesList(Resource):
    """
    Class that represents the recipes collection.

    Methods:
        get -- returns a list of all recipes
        post -- creates a new recipe
    """

    @api.marshal_list_with(recipe_model)
    def get(self):
        """
        Return all recipes

        Returns:
            A list of recipes.
        """
        all_recipes = Recipe.query.all()
        return all_recipes

    @jwt_required()
    @api.expect(recipe_model)
    @api.marshal_with(recipe_model)
    def post(self):
        """
        Create a new recipe

        Returns:
            The newly created recipe.
        """
        if not request.is_json:
            return {"message": "Content-Type must be application/json"}, 400

        # Aquire the recipe data from the requests from the clients
        data = request.get_json()

        title = data.get("title")
        description = data.get("description")

        if not title or not description:
            return {"message": "Title and description are required"}, 400

        new_recipe = Recipe(title=title, description=description)
        new_recipe.save()
        return new_recipe, 201


# endregion All Recipes


# region Single Recipe
@api.route("/recipe/<recipe_id>")
class RecipeResource(Resource):
    """
    Class that represents a single recipe.

    Methods:
        get -- returns a single recipe by id
        put -- updates a single recipe by id
        delete -- deletes a single recipe by id
    """

    @api.marshal_with(recipe_model)
    def get(self, recipe_id):
        """
        Return a single recipe by id

        Parameters:
            recipe_id (string): The id of the recipe to retrieve

        Returns:
            The requested recipe
        """
        recipe = Recipe.query.get_or_404(recipe_id)
        return recipe

    @jwt_required()
    @api.marshal_with(recipe_model)
    def put(self, recipe_id):
        """
        Update a single recipe by id

        Parameters:
            recipe_id (string): The id of the recipe to update
            data (object): A JSON object containing the updated recipe data

        Returns:
            The updated recipe
        """
        recipe = Recipe.query.get_or_404(recipe_id)
        data = request.get_json()
        recipe.update(data.get("title"), data.get("description"))
        return recipe

    @jwt_required()
    @api.marshal_with(recipe_model)
    def delete(self, recipe_id):
        """
        Delete a single recipe by id

        Parameters:
            recipe_id (string): The id of the recipe to delete

        Returns:
            A JSON object with a message indicating the recipe was deleted
        """
        recipe = Recipe.query.get_or_404(recipe_id)
        recipe.delete()
        return recipe, 200


# endregion Single Recipe


if __name__ == "__main__":
    app.run()
