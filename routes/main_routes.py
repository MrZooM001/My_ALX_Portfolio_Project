#!/usr/bin/python3
"""
Module that contains the main blueprint for the Flask application.
It contains the routes for the main page, landing page, and profile page.
"""
from flask import Blueprint, render_template, redirect, url_for
from decouple import config
import requests
import json
from flask_login import login_required, current_user
from sqlalchemy import desc
from models import Recipe, Category

main_bp = Blueprint("main_bp", __name__)


# region Main Page for logged users
@main_bp.route("/main")
@login_required
def main():
    """
    This function serves as the main page for the application. It
    displays a list of recipes based on the user's search criteria.

    Returns:
        A rendered HTML template with the list of recipes by category 
    """
    main_recipes = get_recipe_by_category("Main Course")
    bakery_recipes = get_recipe_by_category("Bakery")
    dessert_recipes = get_recipe_by_category("Dessert")
    sides_recipes = get_recipe_by_category("Side Dish")
    appetizer_recipes = get_recipe_by_category("Appetizer")
    latest_recipes = Recipe.query.order_by(desc(Recipe.created_at)).all()

    return render_template(
        "index.html",
        recipes=main_recipes,
        bakery=bakery_recipes,
        dessert=dessert_recipes,
        sides=sides_recipes,
        appetizer=appetizer_recipes,
        latest_recipes=latest_recipes,
        user=current_user
    )


# endregion Main Page for logged users


# region Landing Page for guests 
@main_bp.route("/")
def landing_page():
    """
    Function serves as the landing page for the application. It
    displays a list of recipes based on third-party API.

    Returns:
        A rendered HTML template as landing page with a list of recipes from API
        or the main page if the current user is logged in.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.main"))
    else:
        api_result = []
        url = "https://api.spoonacular.com/recipes/complexSearch"
        params = {
            "apiKey": config("API_KEY"),
            "query": "*",
            "type": "main course",
            "sort": "popularity",
            "number": 8,
        }
        spoonac_api = requests.get(url, params)
        data = json.loads(spoonac_api.content)
        try:
            recipes = data["results"]
            for item in recipes:
                api_result.append(item)
        except Exception as e:
            print(e)
        return render_template("landing_page.html", data=api_result)


# endregion Landing Page for guests 


# region Profile Page
@main_bp.route("/profile")
@login_required
def profile():
    """
    Function serves as the profile page for the application. It
    displays a list of recipes created by the current logged user.

    Returns:
        A rendered HTML template with the list of the user's recipes.
    """
    my_recipes = Recipe.query.filter(Recipe.user_id == current_user.id).all()
    return render_template(
        "profile.html", my_recipes=my_recipes
    )


# endregion Profile Page


# region Helper Methods
def get_recipe_by_category(category_name):
    """
    Function as helper method that retrieves a list of recipes based on
    the given category name as a parameter.

    Parameters:
        category_name (str): The name of the category for which recipes are to be retrieved.

    Returns:
        A list of Recipe objects that belong to the specified category
        or empty list if there's no category with the given name.
    """
    category = Category.query.filter_by(name=category_name).first()
    if category:
        recipes = Recipe.query.filter_by(category_id=category.id).all()
        return recipes
    else:
        return []


# endregion Helper Methods
