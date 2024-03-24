#!/usr/bin/python3
from extensions import db

class RecipeIngredient(db.Model):
    __tablename__ = "recipes_ingredients"
    recipe_id = db.Column(db.String(60), db.ForeignKey('recipes.id'), nullable=False, primary_key=True)
    ingredient_id = db.Column(db.String(60), db.ForeignKey('ingredients.id'), nullable=False, primary_key=True)
    