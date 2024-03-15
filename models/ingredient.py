#!/usr/bin/python3
from .base_model import BaseModel
from extensions import db

class Ingredient(BaseModel, db.Model):
    __tablename__ = "ingredients"
    name = db.Column(db.String(120), nullable=False, unique=True)
    imgUrl = db.Column(db.Text(), nullable=False)
    # many to many relationship between Recipe & Ingredient
    recipes = db.relationship("RecipeIngredient", back_populates="ingredients")


    def __repr__(self):
        return "<Ingredient {}>".format(self.name)
