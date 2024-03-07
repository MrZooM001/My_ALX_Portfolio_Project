#!/usr/bin/python3
from models.recipe import Recipe
from flask_restx import Namespace, Resource
from flask import request
from flask_jwt_extended import jwt_required
from flask_restx import fields, Resource


recipe_namespace = Namespace(
    "Recipes", description="Namespace for recipes"
)

recipe_model = recipe_namespace.model(
    "Recipe",
    {
        "id": fields.String(),
        "title": fields.String(),
        "description": fields.String()
    }
)


# region All Recipes
@recipe_namespace.route("/recipes")
class RecipesList(Resource):
    """
    Class that represents the recipes collection.

    Methods:
        get -- returns a list of all recipes
        post -- creates a new recipe
    """

    @recipe_namespace.marshal_list_with(recipe_model)
    def get(self):
        """
        Return all recipes

        Returns:
            A list of recipes.
        """
        all_recipes = Recipe.query.all()
        return all_recipes

    @jwt_required()
    @recipe_namespace.expect(recipe_model)
    @recipe_namespace.marshal_with(recipe_model)
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
@recipe_namespace.route("/recipe/<recipe_id>")
class RecipeResource(Resource):
    """
    Class that represents a single recipe.

    Methods:
        get -- returns a single recipe by id
        put -- updates a single recipe by id
        delete -- deletes a single recipe by id
    """

    @recipe_namespace.marshal_with(recipe_model)
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
    @recipe_namespace.marshal_with(recipe_model)
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
    @recipe_namespace.marshal_with(recipe_model)
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
