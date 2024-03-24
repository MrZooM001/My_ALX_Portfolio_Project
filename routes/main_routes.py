from flask import Blueprint, render_template, redirect, url_for
from extensions import db
from decouple import config
import requests
import json
from flask_login import (
    login_required,
    current_user,
)
from models import Recipe, FavoriteRecipe

main_bp = Blueprint('main_bp', __name__)



# region Main Page
@main_bp.route("/main")
@login_required
def main():
    api_bft = []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    bf_params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "breakfast",
        # "maxReadyTime": 15,
        "sort": "popularity",
        "number": 3,
    }
    spoonac_api = requests.get(url, bf_params)
    data = json.loads(spoonac_api.content)
    try:
        bf_recipes = data["results"]
        for item in bf_recipes:
            api_bft.append(item)
    except Exception as e:
        print(e)

    api_apz = []
    apz_params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "appetizer",
        # "maxReadyTime": 15,
        "sort": "popularity",
        "number": 3,
    }
    spoonac_api = requests.get(url, apz_params)
    data = json.loads(spoonac_api.content)
    try:
        apz_recipes = data["results"]
        for item in apz_recipes:
            api_apz.append(item)
    except Exception as e:
        print(e)

    api_sld = []
    sld_params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "salad",
        # "maxReadyTime": 15,
        "sort": "time",
        "number": 3,
    }
    spoonac_api = requests.get(url, sld_params)
    data = json.loads(spoonac_api.content)
    try:
        sld_recipes = data["results"]
        for item in sld_recipes:
            api_sld.append(item)
    except Exception as e:
        print(e)

    api_sld = []
    sld_params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "salad",
        # "maxReadyTime": 15,
        "sort": "time",
        "number": 3,
    }
    spoonac_api = requests.get(url, sld_params)
    data = json.loads(spoonac_api.content)
    try:
        sld_recipes = data["results"]
        for item in sld_recipes:
            api_sld.append(item)
    except Exception as e:
        print(e)

    return render_template("index.html", brkfst=api_bft, sld=api_sld, aptz=api_apz)


# endregion Main Page


# region Landing Page
@main_bp.route("/")
def landing_page():
    if current_user.is_authenticated:
        return redirect(url_for('main_bp.main'))
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
