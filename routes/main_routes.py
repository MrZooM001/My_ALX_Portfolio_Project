from flask import Blueprint, render_template, redirect, url_for
from extensions import db
from decouple import config
import requests
import json
from flask_login import (
    login_required,
    current_user,
)
from models import Recipe, FavoriteRecipe, Category

main_bp = Blueprint("main_bp", __name__)


# region Main Page
@main_bp.route("/main")
@login_required
def main():
    main_recipes = get_recipe_by_category("Main Course")
    bakery_recipes = get_recipe_by_category("Bakery")
    dessert_recipes = get_recipe_by_category("Dessert")
    sides_recipes = get_recipe_by_category("Side Dish")

    return render_template(
        "index.html",
        recipes=main_recipes,
        bakery=bakery_recipes,
        dessert=dessert_recipes,
        sides=sides_recipes,
    )


# endregion Main Page


# region Landing Page
@main_bp.route("/")
def landing_page():
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


# endregion Landing Page


# region Profile Page
@main_bp.route("/profile")
@login_required
def profile():
    favorites = (
        db.session.query(Recipe)
        .join(FavoriteRecipe)
        .filter(FavoriteRecipe.user_id == current_user.id)
        .all()
    )

    my_recipes = Recipe.query.filter(Recipe.user_id == current_user.id).all()

    return render_template(
        "profile.html", data=favorites, my_recipes=my_recipes, user=current_user
    )


# endregion Profile Page


# region Helper Methods
def get_recipe_by_category(category_name):
    category = Category.query.filter_by(name=category_name).first()
    if category:
        recipes = Recipe.query.filter_by(category_id=category.id).all()
        return recipes
    else:
        return None


# endregion Helper Methods
