#!/usr/bin/python3
"""
Module contains the blueprint for the recipes section of the application.
It contains the routes for the recipe page, adding & editing a recipe.
It also contains the forms for adding & editing recipes.
"""

from datetime import datetime
from flask import Blueprint, redirect, render_template, url_for, request, jsonify
from extensions import db
from flask_login import login_required, current_user
from models import Ingredient, Recipe, Step, Category
from forms import SearchForm


search_bp = Blueprint("search_bp", __name__)

@search_bp.route('/search', methods=["POST"])
@login_required
def search():
    if request.referrer is None and request.endpoint != 'static':
        return redirect(url_for('main_bp.landing_page'))
    form = SearchForm()
    recipes = Recipe.query
    if form.validate_on_submit():
        recipe_searched = form.searched.data
        print("######################################################################################\n")
        print()
        print("\n######################################################################################")

        recipes = recipes.filter(Recipe.title.like("%" + recipe_searched + "%") | Recipe.ingredients.any(Ingredient.ingredient_name.like("%" + recipe_searched + "%")))
        recipes = recipes.order_by(Recipe.created_at.desc()).limit(25).all()

    return render_template("search.html", form=form, recipes=recipes)
