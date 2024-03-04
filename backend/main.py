""" Module to configure flask application """

from config import DevConfig
from extentions import db
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
from models import Recipe
import requests


app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
api = Api(app, doc="/docs")

recipe_model = api.model(
    "Recipe",
    {"id": fields.String(), "title": fields.String(), "description": fields.String()},
)


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


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "Recipe": Recipe}


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
