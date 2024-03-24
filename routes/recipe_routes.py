from flask import Blueprint, redirect, render_template, url_for
from extensions import db
from flask_login import login_required, current_user
from models import Ingredient, Recipe, Step, Category
from forms import RecipeForm, IngredientForm, StepsForm

recipes_bp = Blueprint("recipes_bp", __name__)


# region Recipe Page
@recipes_bp.route("/<recipe_title>", methods=["GET"])
@login_required
def recipe(recipe_title):
    recipe = Recipe.query.filter_by(
        title=recipe_title.replace("_", " ")).first()

    return render_template("recipe.html", recipe=[recipe])


# endregion Recipe Details Page


# region Add Recipe
@recipes_bp.route("/add-recipe", methods=["GET", "POST"], strict_slashes=False)
@login_required
def add_recipe():
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
                unit=ingred["unit"],
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
        page_title=page_title
    )


# endregion Add Recipe


# region Add Categories
def add_cats():
    db.session.add_all(
        [
            Category(name="Main Course"),
            Category(name="Side Dish"),
            Category(name="Breakfast"),
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
