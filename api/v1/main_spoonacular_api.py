#!/usr/bin/python3
""" Module to configure flask application """

from api.v1.config import DevConfig
from models.recipe import Recipe
from api.v1.extentions import db
from decouple import config
from flask import Flask, jsonify, request
from flask_restx import Api, Resource, fields
import requests


app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
api = Api(app, doc="/docs")


# region Hello World
@api.route("/hello")
class Helo(Resource):
    def get(self):
        """
        Returns a simple test message in JSON format

        Returns:
            dict: JSON object containing the greeting message
        """
        return {"message": "Hello World!"}


# endregion Hello World

# region All Recipes
@api.route("/recipes")
class RecipesList(Resource):
    # @api.marshal_list_with(recipe_model)
    def get(self):
        """Get all recipes"""
        url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": config("API_KEY"),
            "query": "pizza",
            # "type": "soup",
            # "maxReadyTime": 15,
            "sort": "popularity",
            "number": 5,
        }
        spoonac_api = requests.get(url, params)
        return spoonac_api.json()

    def post_recipe(self):
        """Create a new recipe"""
        pass


# endregion All Recipes


# region Single Recipe
@api.route("/recipe/<recipe_id>")
class RecipeResource(Resource):
    def get(self, recipe_id):
        """Get a recipe by id"""
        # url = "https://api.spoonacular.com/recipes/{}/summary".format(recipe_id)
        url = "https://api.spoonacular.com/recipes/{}/information".format(recipe_id)
        params = {
            "apiKey": config("API_KEY"),
            "query": "burgers",
            "sort": "popularity",
            "number": 3,
        }
        spoonac_api = requests.get(url, params)
        return spoonac_api.json()
        pass

    def put(self, recipe_id):
        """Update a recipe by id"""
        pass

    def delete(self, recipe_id):
        """Delete a recipe by id"""
        pass


# endregion Single Recipe


if __name__ == "__main__":
    app.run()
