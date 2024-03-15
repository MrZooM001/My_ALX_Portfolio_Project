#!/usr/bin/python3
from extensions import db

class RecipeIngredient(db.Model):
    __tablename__ = "recipes_ingredients"
    recipe_id = db.Column(db.String(60), db.ForeignKey('recipes.id'), nullable=False, primary_key=True)
    ingredient_id = db.Column(db.String(60), db.ForeignKey('ingredients.id'), nullable=False, primary_key=True)
    quantity = db.Column(db.String(60), db.ForeignKey('quantities.id'), nullable=False)
    unit = db.Column(db.String(60), db.ForeignKey('measurement_units.id'), nullable=False)

    recipes = db.relationship("Recipe", back_populates="ingredients")
    
    ingredients = db.relationship("Ingredient", back_populates="recipes")
