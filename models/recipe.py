#!/usr/bin/python3
"""
Module defines the database schema for the recipes table.
"""
from .base_model import BaseModel
from extensions import db


class Recipe(BaseModel, db.Model):
    """
    This class represents a recipe in the database.
    
    Args:
        db (SQLAlchemy object): The SQLAlchemy object that is used to interact with the database.

    Attributes:
        title (str): The title of the recipe.
        imgUrl (str): The URL of the image of the recipe.
        servings (int): The number of servings the recipe makes.
        readyInMinutes (int): The estimated time it takes to prepare the recipe.
        preparationMinutes (int): The estimated time it takes to prepare the recipe.
        cookingMinutes (int): The estimated time it takes to cook the recipe.
        description (str): A description of the recipe.
        is_approved (bool): A boolean indicating whether the recipe has been approved or not.
        ingredients (list): A list of ingredients used in the recipe.
        user_id (str): The ID of the user who created the recipe.
        user (User): The user who created the recipe.
        category_id (str): The ID of the category the recipe belongs to.
        category (Category): The category object the recipe belongs to.
    """
    __tablename__ ='recipes'
    title = db.Column(db.String(120), nullable=False, unique=True)
    imgUrl = db.Column(db.Text(), nullable=False)
    servings = db.Column(db.Integer(), nullable=False)
    readyInMinutes = db.Column(db.Integer(), nullable=False)
    preparationMinutes = db.Column(db.Integer(), nullable=False)
    cookingMinutes = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    is_approved = db.Column(db.Boolean(), default=False)

    ingredients = db.relationship("Ingredient", secondary="recipes_ingredients", backref=db.backref('recipes', lazy='dynamic', collection_class=list))

    user_id = db.Column(db.String(60), db.ForeignKey('users.id'))
    user = db.relationship("User", backref=db.backref("recipes", lazy="dynamic"))

    category_id = db.Column(db.String(60), db.ForeignKey('categories.id'))
    category = db.relationship("Category", backref="recipes")

    def __repr__(self):
        return "<Recipe {}\nDescription {}>".format(self.title, self.description)
