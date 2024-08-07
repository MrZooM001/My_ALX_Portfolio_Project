#!/usr/bin/python3
"""
Module defines the recipe form for both add & edit a recipe.
"""

from models import Recipe
from flask_wtf import FlaskForm
from wtforms import (
    StringField, TextAreaField,
    IntegerField, Form, SelectField,
    FieldList, FormField, FloatField
)
from wtforms.validators import InputRequired, Length, ValidationError, NumberRange
from models import Category



class IngredientForm(Form):
    """
    Class defines the subform for adding or editing an ingredient.
    
    Attributes:
        ingredient_name (wtforms.fields.StringField): The name of the ingredient.
        quantity (wtforms.fields.DecimalField): The quantity of the ingredient.
        unit (wtforms.fields.StringField): The unit of the ingredient.
    """
    ingredient_name = StringField("Ingredient Name", validators=[InputRequired(), Length(min=1, max=120)], render_kw={"placeholder": "Ingredient Name"})
    quantity = FloatField("Quantity", validators=[InputRequired(), NumberRange(min=0, max=3000.0)], render_kw={"placeholder": "Quantity"})
    unit = StringField("Unit", validators=[InputRequired(), Length(min=1, max=20)], render_kw={"placeholder": "Unit"})


class StepsForm(Form):
    """
    Class defines the subform for adding or editing an ingredient.
    
    Attributes:
        instruction (wtforms.fields.TextAreaField): The instruction of the recipe step.
    """
    instruction = TextAreaField("Recipe Steps", render_kw={"placeholder": "Recipe Steps"})


class RecipeForm(FlaskForm):
    """
    Class defines the main form for adding or editing a recipe.
    
    Attributes:
        All available Recipe attributes.

    Raises:
        ValidationError: If the title of the recipe is already in use.
    """

    title = StringField("Recipe Title", validators=[InputRequired(), Length(min=1, max=120)], render_kw={"placeholder": "Recipe Title"})
    imgUrl =  StringField("Image URL", validators=[InputRequired(), Length(min=1)], render_kw={"placeholder": "Image URL"})
    servings = IntegerField("Servings", validators=[InputRequired(), NumberRange(min=1, max=500)], render_kw={"placeholder": "Servings"})
    readyInMinutes = IntegerField("Ready In Time", validators=[InputRequired(), NumberRange(min=0, max=2400)], render_kw={"placeholder": "Ready In Time"})
    preparationMinutes = IntegerField("Preparation Time", validators=[InputRequired(), NumberRange(min=0, max=2400)], render_kw={"placeholder": "Preparation Time"})
    cookingMinutes = IntegerField("Cooking Time", validators=[InputRequired(), NumberRange(min=0, max=2400)], render_kw={"placeholder": "Cooking Time"})
    description = TextAreaField("Description", render_kw={"placeholder": "Description"})
    ingredients = FieldList(FormField(IngredientForm), min_entries=1, max_entries=120)
    steps = FieldList(FormField(StepsForm), min_entries=1, max_entries=120)
    category = SelectField("Category")

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        self.category.choices = [(cat.id, cat.name) for cat in Category.query.order_by(Category.name).all()]

    def validate_recipe(self, title):
        existing_recipe = Recipe.query.filter_by(title=title).first()

        if existing_recipe:
            raise ValidationError("A recipe with the same title already exists")
        