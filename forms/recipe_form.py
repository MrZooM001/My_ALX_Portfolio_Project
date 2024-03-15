from models import Recipe
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, FieldList, FormField, DecimalField
from wtforms.validators import InputRequired, Length, ValidationError


class IngredientForm(FlaskForm):
    name = StringField("Ingredient Name",
        validators=[InputRequired(), Length(min=2, max=80)],
        render_kw={"placeholder": "Ingredient Name"}
    )
    imgUrl = TextAreaField("Ingredient Image URL",
        validators=[InputRequired(), Length(min=2)],
        render_kw={"placeholder": "Ingredient Image URL"}
    )
    quantity = DecimalField("Ingredient Quantity",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ingredient Quantity"}
    )
    unit = StringField("Measurement Unit",
        validators=[InputRequired(), Length(min=1, max=18)],
        render_kw={"placeholder": "Measurement Unit"}
    )


class StepForm(FlaskForm):
    instruction = TextAreaField("Recipe Steps",
        validators=[InputRequired(), Length(min=1)],
        render_kw={"placeholder": "Recipe Steps"}
    )



class RecipeForm(FlaskForm):
    """Add a new Recipe"""
    ingredient_label = StringField("Add Ingredient")
    form_label = StringField("Add Recipe")
    title = StringField("Recipe Title",
        validators=[InputRequired(), Length(min=4, max=100)],
        render_kw={"placeholder": "Recipe Title"},
    )
    imgUrl = TextAreaField("Recipe Image URL",
        validators=[InputRequired(), Length(min=4)],
        render_kw={"placeholder": "Recipe Image URL"},
    )
    servings = IntegerField("Servings Count",
        validators=[InputRequired()],
        render_kw={"placeholder": "Servings"},
    )
    readyInMinutes = IntegerField("Ready In Time",
        validators=[InputRequired()],
        render_kw={"placeholder": "Ready In Minutes"},
    )
    preparationMinutes = IntegerField("Preparation Time",
        validators=[InputRequired()],
        render_kw={"placeholder": "Preparation Time"},
    )
    cookingMinutes = IntegerField("Cooking Time",
        validators=[InputRequired()],
        render_kw={"placeholder": "Cooking Time"},
    )
    description = TextAreaField("Description",
        validators=[InputRequired()],
        render_kw={"placeholder": "Description"},
    )
    ingredients = FieldList(FormField(IngredientForm), min_entries=1)

    steps = FieldList(FormField(StepForm), min_entries=1)

    submit = SubmitField("Add Recipe")

    def validate_recipe(self, title):
        existing_recipe = Recipe.query.filter_by(title=title).first()

        if existing_recipe:
            raise ValidationError("A recipe with the same title already exists")


class LoadRecipeForm(FlaskForm):
    """Load a new Recipe from database"""
    title = StringField(
        validators=[InputRequired(), Length(min=4, max=100)],
        render_kw={"placeholder": "Username"},
    )

    submit = SubmitField("Load Recipe")
