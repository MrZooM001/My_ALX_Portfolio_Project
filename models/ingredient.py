#!/usr/bin/python3
from .base_model import BaseModel
from extensions import db

class Ingredient(BaseModel, db.Model):
    __tablename__ = "ingredients"
    ingredient_name = db.Column(db.String(120), nullable=False)
    quantity = db.Column(db.Float(), nullable=False)
    unit = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return "<Ingredient {}>".format(self.ingredient_name)
