#!/usr/bin/python3
from .base_model import BaseModel
from extensions import db

class IngredientQuantity(BaseModel, db.Model):
    __tablename__ = "ingredient_quantity"
    recipe_id = db.Column(db.Integer(), db.ForeignKey('recipes.id'), nullable=False)  # Foreign key data type corrected
    ingredient_id = db.Column(db.Integer(), db.ForeignKey('ingredients.id'), nullable=False)  # Foreign key data type corrected
    quantity = db.Column(db.Float(), nullable=False)
    ingredient = db.relationship('Ingredient', back_populates='ingredient_quantities')  # Backref corrected

    def __repr__(self):
        return "<Ingredient Quantity: {}>".format(self.quantity)
