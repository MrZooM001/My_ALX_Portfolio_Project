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


    # many to many relationship between Recipe & Ingredient
    ingredients = db.relationship("RecipeIngredient", back_populates="recipes")

    # one to one relationship between Recipe & Description
    steps = db.relationship("Step", backref='recipes', uselist=False)

    users = db.relationship("UserFavorite", back_populates="recipes")



    def __repr__(self):
        return "<Recipe {}\nDescription {}>".format(self.title, self.description)

    def save(self):
        db.session.add(self)
        db.session.commit()
