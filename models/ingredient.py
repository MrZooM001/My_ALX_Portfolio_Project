#!/usr/bin/python3
"""
Module defines the Ingredient class, which represents a single ingredient in a recipe.
"""
from .base_model import BaseModel
from extensions import db

class Ingredient(BaseModel, db.Model):
    """
    Class represents a ingredients in the database.

    Args:
        db (SQLAlchemy object): The SQLAlchemy object that is used to interact with the database.

    Attributes:
        ingredient_name (string): The name of the ingredient
        quantity (float): The quantity of the ingredient required
        unit (string): The unit of measurement for the ingredient
    """
    __tablename__ = "ingredients"
    ingredient_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Float(), nullable=False)
    unit = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return "<Ingredient {}>".format(self.ingredient_name)
