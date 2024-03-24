#!/usr/bin/python3
from .base_model import BaseModel
from extensions import db


class Recipe(BaseModel, db.Model):
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
