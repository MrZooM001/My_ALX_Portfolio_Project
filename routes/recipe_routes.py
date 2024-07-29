#!/usr/bin/python3
"""
Module contains the blueprint for the recipes section of the application.
It contains the routes for the recipe page, adding & editing a recipe.
It also contains the forms for adding & editing recipes.
"""

from datetime import datetime
from flask import Blueprint, redirect, render_template, url_for, request
from extensions import db
from flask_login import login_required, current_user
from models import Ingredient, Recipe, Step, Category
from forms import RecipeForm, IngredientForm, StepsForm
from fractions import Fraction


recipes_bp = Blueprint("recipes_bp", __name__)


# region Recipe Page
@recipes_bp.route("/<recipe_title>", methods=["GET"])
@login_required
def recipe(recipe_title):
    """
    Returns the recipe with the given title.
    
    Args:
        recipe_title (str): The title of the recipe.

    Returns:
        The recipe object with the given title.

    Raises:
        HTTPException: If the recipe does not exist.
    """
    recipe = Recipe.query.filter_by(title=recipe_title.replace("_", " ")).first()

    return render_template("recipe.html", recipe=[recipe], convert_point_fraction=convert_point_fraction)


# endregion Recipe Details Page


# region Add Recipe
@recipes_bp.route("/add-recipe", methods=["GET", "POST"], strict_slashes=False)
@login_required
def add_recipe():
    """
    Function to add a new recipe to the database through a form.

    Returns:
        A redirect to the user's profile page updated list of recipes
        with the new recipe, or re-render the form page if there's an error.
    """
    categories = Category.query.all()
    if not categories:
        add_categories()

    page_title = "Add Recipe"
    form = RecipeForm()
    ingredients_template_form = IngredientForm(prefix="ingredients-_-")
    steps_template = StepsForm(prefix="steps-_-")

    if form.validate_on_submit():
        category = Category.query.filter_by(id=form.category.data).first()
        new_recipe = Recipe(
            title=form.title.data,
            imgUrl=form.imgUrl.data,
            servings=form.servings.data,
            readyInMinutes=int(form.readyInMinutes.data),
            preparationMinutes=int(form.preparationMinutes.data),
            cookingMinutes=int(form.cookingMinutes.data),
            description=form.description.data,
            category=category,
            user=current_user,
        )

        db.session.add(new_recipe)

        for ingred in form.ingredients.data:
            new_ingredient = Ingredient(
                ingredient_name=ingred["ingredient_name"],
                quantity=ingred["quantity"],
                unit=ingred["unit"]
            )
            new_recipe.ingredients.append(new_ingredient)

        for step in form.steps.data:
            new_step = Step(instruction=step["instruction"])
            new_recipe.steps.append(new_step)

        db.session.commit()
        return redirect(url_for("main_bp.profile"))

    return render_template(
        "add_recipe.html",
        form=form,
        _template=ingredients_template_form,
        steps_template=steps_template,
        page_title=page_title,
        url_back=request.referrer
    )


# endregion Add Recipe


# region Update a Recipe
@recipes_bp.route("/edit-recipe/<recipe_id>", methods=["GET", "POST"], strict_slashes=False)
def edit_recipe(recipe_id):
    """
    Function allows the user to edit its own and an existing recipe in the database.
    
    Args:
        recipe_id (str): The ID as UUID of the recipe to be edited.

    Returns:
        A redirect to the recipe page updated with the new data,
        or re-render the same form page if there's an error.

    Raises:
        HTTPException: If the recipe does not exist.
    """
    recipe = db.session.scalars(db.select(Recipe).filter_by(id=recipe_id)).first()

    form = RecipeForm(request.form, obj=recipe)

    ingredients_template = IngredientForm(prefix="ingredients-_-")
    steps_template = StepsForm(prefix="steps-_-")

    ingredients_entries = []
    for ingred in recipe.ingredients:
        ingredients_form = IngredientForm(ingredient_name=ingred.ingredient_name, quantity=ingred.quantity, unit=ingred.unit)
        ingredients_entries.append(ingredients_form)

    ingredients_template.entries = ingredients_entries

    steps_entries = []
    for step in recipe.steps:
        steps_form = StepsForm(instruction=step.instruction)
        steps_entries.append(steps_form)

    steps_template.entries = steps_entries

    category = Category.query.filter_by(id=recipe.category.id).first()
    form.category.data = category.id

    if form.validate_on_submit():
        for ingredient in recipe.ingredients:
            db.session.delete(ingredient)

        for step in recipe.steps:
            db.session.delete(step)

        db.session.commit()

        recipe.title=form.title.data
        recipe.imgUrl=form.imgUrl.data
        recipe.servings=form.servings.data
        recipe.readyInMinutes=form.readyInMinutes.data
        recipe.preparationMinutes=form.preparationMinutes.data
        recipe.cookingMinutes=form.cookingMinutes.data
        recipe.description=form.description.data
        recipe.category = category
        recipe.user=current_user

        for ingred in form.ingredients.data:
            new_ingredient = Ingredient(
                ingredient_name=ingred["ingredient_name"],
                quantity=ingred["quantity"],
                unit=ingred["unit"],
            )
            recipe.ingredients.append(new_ingredient)

        for step in form.steps.data:
            new_step = Step(instruction=step["instruction"])
            recipe.steps.append(new_step)

        recipe.updated_at = datetime.now()
        db.session.commit()
        recipe_title_url = recipe.title.replace(" ", "_")
        return redirect(url_for('recipes_bp.recipe', recipe_title=recipe_title_url))

    return render_template('edit_recipe.html',
        recipe=recipe,
        form=form,
        ingredients_template=ingredients_template,
        steps_template=steps_template, url_back=request.referrer)

# endregion Update a Recipe


# region Delete a Recipe, including related ingredients & steps
@recipes_bp.route("/delete-recipe/<recipe_id>", methods=["GET", "POST"], strict_slashes=False)
def delete_recipe(recipe_id):
    """
    Function allows the user to delete its own recipe from the database.
    
    Args:
        recipe_id (str): The ID as UUID of the recipe to be edited.

    Returns:
        A redirect to the profile page after deleting recipe.

    Raises:
        HTTPException: If the recipe does not exist.
    """
    recipe = db.session.scalars(db.select(Recipe).filter_by(id=recipe_id)).first()

    recipe_title = recipe.title

    for ingredient in recipe.ingredients:
        db.session.delete(ingredient)

    for step in recipe.steps:
        db.session.delete(step)

    db.session.delete(recipe)
    db.session.commit()

    return redirect(url_for('main_bp.profile', recipe_title=recipe_title))


# endregion Delete a Recipe


# region Toggle Favorite Recipe
@recipes_bp.route('/toggle-favorite/<recipe_id>', methods=['POST'])
def toggle_favorite(recipe_id):
    """
    Function allows the user to add or remove a recipe from their favorites list.

    Args:
        recipe_id (str): The ID as UUID of the recipe to add or remove from the favorites list.

    Returns:
        A redirect to the user's profile page and marks the recipe as favorite.

    Raises:
        HTTPException: If the recipe does not exist.
    """
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe in current_user.favorites:
        current_user.favorites.remove(recipe)
    else:
        current_user.favorites.append(recipe)
    db.session.commit()
    return redirect(url_for("main_bp.profile", recipe_id=recipe_id))


# endregion Toggle Favorite Recipe


# region List Favorite Recipe
@recipes_bp.route('/favorites', methods=['GET'])
def favorites():
    """
    Returns a list of all the recipes that the user has marked as favorites.
    """
    all_favorites = current_user.favorites
    return render_template("favorites.html", favorites=all_favorites)

# endregion List Favorite Recipe


# region Add Categories
def add_categories():
    """
    Function as helper method to add all the initial categories to the database.
    """
    db.session.add_all(
        [
            Category(name="Main Course"),
            Category(name="Side Dish"),
            Category(name="Breakfast"),
            Category(name="Dinner"),
            Category(name="Dessert"),
            Category(name="Appetizer"),
            Category(name="Salad"),
            Category(name="Bakery"),
            Category(name="Soup"),
            Category(name="Drink"),
            Category(name="Sauce"),
            Category(name="Marinade"),
        ]
    )
    db.session.commit()
    return "Categories Added successfully"


# endregion Add Categories

# region convert float point number to fraction symbol
def convert_point_fraction(number):
    """
    Function as helper method to convert float point number to
    fraction symbol.

    Args:
        number (float): the given float number to convert.
    
    example:
    >>> convert_point_fraction(2.25)
    >>> 2 1/4
    or
    >>> convert_point_fraction(0.750)
    >>> 3/4
    """
    integer_left, fractional_right = str(number).split('.')
    integer_left = int(integer_left)
    fractional_right = int(fractional_right)

    if fractional_right == 0:
        return integer_left
    elif integer_left > 0:
        fraction = Fraction(fractional_right, 10**len(str(fractional_right)))
        return "{} {}/{}".format(integer_left, fraction.numerator, fraction.denominator)
    else:
        fraction = Fraction(fractional_right, 10**len(str(fractional_right)))
        return "{}/{}".format(fraction.numerator, fraction.denominator)


# endregion convert to fraction