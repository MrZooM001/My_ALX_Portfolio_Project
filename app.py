from flask import (
    Flask,
    flash,
    make_response,
    render_template,
    request,
    url_for,
    redirect,
    session,
    jsonify,
)
from extensions import db
from config import DevConfig
from flask_migrate import Migrate
from decouple import config
import requests
import json
from flask_login import (
    login_user,
    login_required,
    LoginManager,
    logout_user,
    current_user,
)
from models import (
    User,
    Recipe,
    Ingredient,
    RecipeIngredient,
    Step,
    MeasurementUnit,
    Quantity,
)
from forms import LoginForm, RegisterForm, RecipeForm, LoadRecipeForm
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os


app = Flask(__name__)

app.config.from_object(DevConfig)

db.init_app(app)

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.session_protection = "strong"


# region

# endregion


@app.route("/recipes", methods=["GET"])
@login_required
def all_recipes():
    """Get all recipes from spoonacular"""
    api_result = []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": config("API_KEY"),
        "query": '*',
        "type": "side dish",
        # "maxReadyTime": 15,
        "sort": "popularity",
        "number": 24,
    }
    spoonac_api = requests.get(url, params)
    data = json.loads(spoonac_api.content)
    try:
        recipes = data["results"]
        for item in recipes:
                api_result.append(item)
    except Exception as e:
        print(e)
        

    return render_template("search_recipes.html", data=api_result)


@app.route("/recipes/dessert", methods=["GET"])
@login_required
def recipes_dessert():
    """Get top 10 dessert from spoonacular"""
    api_result = []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "dessert",
        # "maxReadyTime": 15,
        "sort": "popularity",
        "number": 20,
    }
    spoonac_api = requests.get(url, params)
    data = json.loads(spoonac_api.content)
    try:
        recipes = data["results"]
        for item in recipes:
            api_result.append(item)
    except Exception as e:
        print(e)

    return render_template("recipes_dessert.html", data=api_result)


@app.route("/popular", methods=["GET"])
@login_required
def popular():
    """Get top 10 dessert from spoonacular"""
    api_result = []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "dessert",
        # "maxReadyTime": 15,
        "sort": "popularity",
        "number": 20,
    }
    spoonac_api = requests.get(url, params)
    data = json.loads(spoonac_api.content)
    try:
        recipes = data["results"]
        for item in recipes:
            api_result.append(item)
    except Exception as e:
        print(e)

    return render_template("popular.html", data=api_result)


@app.route("/recipes/main", methods=["GET"])
@login_required
def recipes_main():
    """Get top 10 dessert from spoonacular"""
    api_result = []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "main course",
        # "maxReadyTime": 15,
        "sort": "popularity",
        "number": 20,
    }
    spoonac_api = requests.get(url, params)
    data = json.loads(spoonac_api.content)
    try:
        recipes = data["results"]
        for item in recipes:
            api_result.append(item)
    except Exception as e:
        print(e)

    return render_template("recipes_main_course.html", data=api_result)


@app.route("/recipes/breakfast", methods=["GET"])
@login_required
def recipes_breakfast():
    """Get top 10 dessert from spoonacular"""
    api_result = []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "breakfast",
        # "maxReadyTime": 15,
        "sort": "popularity",
        "number": 20,
    }
    spoonac_api = requests.get(url, params)
    data = json.loads(spoonac_api.content)
    try:
        recipes = data["results"]
        for item in recipes:
            api_result.append(item)
    except Exception as e:
        print(e)
        

    return render_template("recipes_breakfast.html", data=api_result)

@app.route("/recipes/bread", methods=["GET"])
@login_required
def recipes_bread():
    """Get top 10 dessert from spoonacular"""
    api_result = []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "bread",
        # "maxReadyTime": 15,
        "sort": "popularity",
        "number": 20,
    }
    spoonac_api = requests.get(url, params)
    data = json.loads(spoonac_api.content)
    try:
        recipes = data["results"]
        for item in recipes:
            api_result.append(item)
    except Exception as e:
        print(e)
        

    return render_template("recipes_breakfast.html", data=api_result)



# region
# @app.route("/recipes/", methods=["GET", "POST"])
# def add_recipe():
#     form = RecipeForm()
#     if form.validate_on_submit():
#         print("****************************** Validate successful *************************************")
#         print("****************************** Validate successful *************************************")
#         recipe = Recipe.query.filter_by(title=form.title.data).first()
#         if not recipe:
#             ingredients = []
#             for ingredient in form.ingredients.data:
#                 name = ingredient["name"]
#                 imgUrl = ingredient["img_url"]
#                 ingredients.append({"name": name, "url": imgUrl})

#             new_recipe = Recipe(
#                 title=form.title.data,
#                 imgUrl=form.imgUrl.data,
#                 servings=form.servings.data,
#                 readyInMinutes=form.readyInMinutes.data,
#                 preparationMinutes=form.preparationMinutes.data,
#                 cookingMinutes=form.cookingMinutes.data,
#                 description=form.description.data,
#                 users=current_user
#             )
#             db.session.add(new_recipe)

#             steps = []
#             if not form.steps.data:
#                 pass
#             else:
#                 for step in form.steps.data:
#                     instruction = step["instruction"]
#                     steps.append({"instruction": instruction})

#                 for step in steps:
#                     new_step = Step(instruction=step["instruction"])
#                     new_recipe.steps.append(new_step)

#             for ingredient in ingredients:
#                 unit = MeasurementUnit.query.filter_by(name=form.ingredient.unit.data).first()
#                 if not unit:
#                     unit = MeasurementUnit(name=form.ingredients.unit.data)
#                     db.session.add(unit)
#                 quantity = Quantity(amount=form.ingredients.quantity.data)
#                 db.session.add(quantity)

#                 recipe_ingredient = RecipeIngredient(
#                     quantity=ingredient["quantity"], unit=ingredient["unit"]
#                 )
#                 new_recipe.ingredients.append(recipe_ingredient)
#             db.session.commit()
#             return redirect(url_for("recipe.html"))
#     return render_template("add_recipe.html", form=form)
# endregion


@app.route("/add-recipe", methods=["GET", "POST"], strict_slashes=False)
@login_required
def add_recipe():
    form = RecipeForm()
    if request.method == "POST" and form.validate_on_submit():
        recipe = Recipe.query.filter_by(title=form.title.data).first()
        if not recipe:
            new_recipe = Recipe(
                title=form.title.data,
                imgUrl=form.imgUrl.data,
                servings=form.servings.data,
                readyInMinutes=form.readyInMinutes.data,
                preparationMinutes=form.preparationMinutes.data,
                cookingMinutes=form.cookingMinutes.data,
                description=form.description.data,
                user=current_user,
            )
            db.session.add(new_recipe)

            for ingredient_field in form.ingredients:
                ingredient = ingredient_field.data
                name = ingredient["name"]
                imgUrl = ingredient["img_url"]
                quantity = ingredient["quantity"]
                unit_name = ingredient["unit"]

                unit = MeasurementUnit.query.filter_by(name=unit_name).first()
                if not unit:
                    unit = MeasurementUnit(name=unit_name)
                    db.session.add(unit)

                quantity_obj = Quantity(amount=quantity)
                db.session.add(quantity_obj)

                recipe_ingredient = RecipeIngredient(
                    ingredient=Ingredient(name=name, imgUrl=imgUrl),
                    quantity=quantity_obj,
                    unit=unit,
                )
                new_recipe.ingredients.append(recipe_ingredient)

            for step_data in form.steps.data:
                new_step = Step(instruction=step_data["instruction"])
                new_recipe.steps.append(new_step)

            try:
                db.session.commit()
                return redirect(url_for("home"))  # Redirect to the appropriate route
            except Exception as e:
                db.session.rollback()
                flash("An error occurred while adding the recipe: " + str(e), "error")
                return redirect(
                    url_for("recipe")
                )  # Redirect to the add_recipe page if an error occurs
            finally:
                db.session.close()

    return render_template("add_recipe.html", form=form)


@app.route("/recipe", methods=["GET"])
@login_required
def recipe_details():


    api_result = []
    # url = "https://api.spoonacular.com/recipes/complexSearch"
    # spoonac_api = requests.get(url)
    # data = json.loads(spoonac_api.content)
    # try:
    #     recipes = data["results"]
    # except Exception as e:
    #     print(e)
    # for item in recipes:
    #     api_result.append(item)

    return render_template("recipe.html", data=api_result)


# region Home
@app.route("/")
def landing_page():
    api_result = []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "main course",
        # "maxReadyTime": 15,
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
    return render_template("landing.html", data=api_result)



@app.route("/home")
@login_required
def home():
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
    except Exception as e:print(e)

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


# endregion Home


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user = current_user
    api_favo = []
    url = "https://api.spoonacular.com/recipes/complexSearch"
    favo_params = {
        "apiKey": config("API_KEY"),
        "query": "*",
        "type": "bread",
        # "maxReadyTime": 15,
        "sort": "popularity",
        "number": 4,
    }
    spoonac_api = requests.get(url, favo_params)
    data = json.loads(spoonac_api.content)
    try:
        bf_recipes = data["results"]
        for item in bf_recipes:
            api_favo.append(item)
    except Exception as e:
        print(e)

    return render_template("profile.html", user=user, data=api_favo)


# region user access session


# region load user from db
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# endregion load user from db


# region Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    response = make_response(redirect(url_for("landing_page")))
    response.delete_cookie("session")
    return response


# endregion Logout


# region Login
@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("profile"))

    return render_template("login.html", form=form)


# endregion Login


# region signup
@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            username=form.username.data,
            password=bcrypt.generate_password_hash(form.password.data),
        )
        new_user.save()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


# endregion signup

# endregion user access session


if __name__ == "__main__":
    dotenv_file = os.path.join(os.getcwd(), ".env")
    load_dotenv(dotenv_file)
    app.run(debug=True)
