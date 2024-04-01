#!/usr/bin/python3
"""
Module defines the one-to-many relationship between Users and Recipes.
It is used to store the user's favorite recipes.
"""
from extensions import db

class FavoriteRecipe(db.Model):
    """
    Class defines the FavoriteRecipe model.

    Args:
        db (SQLAlchemy object): The SQLAlchemy object that is used to interact with the database.

    Attributes:
        recipe_id (str): The primary key of the recipe_ingredients table,
                        which is a foreign key to the recipes table.
        ingredient_id (str): The primary key of the recipe_ingredients table,
                            which is a foreign key to the ingredients table.
    """
    __tablename__ = "favorite_recipes"
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.String(60), db.ForeignKey('recipes.id'), primary_key=True)
