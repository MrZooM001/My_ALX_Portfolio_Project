#!/usr/bin/python3
"""
Module defines the many-to-many relationship between Recipes and Ingredients.
It is used to store the ingredients in the recipes.
"""
from extensions import db

class RecipeIngredient(db.Model):
    """
    Class represents the many-to-many relationship between Recipes and Ingredients.

    Args:
        db (SQLAlchemy object): The SQLAlchemy object that is used to interact with the database.

    Attributes:
        recipe_id (str): The primary key of the recipe_ingredients table, which is a foreign key to the recipes table.
        ingredient_id (str): The primary key of the recipe_ingredients table, which is a foreign key to the ingredients table.
    """
    __tablename__ = "recipes_ingredients"
    recipe_id = db.Column(db.String(60), db.ForeignKey('recipes.id'), nullable=False, primary_key=True)
    ingredient_id = db.Column(db.String(60), db.ForeignKey('ingredients.id'), nullable=False, primary_key=True)
    