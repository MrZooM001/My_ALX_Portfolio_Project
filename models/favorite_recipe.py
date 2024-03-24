#!/usr/bin/python3
from extensions import db

class FavoriteRecipe(db.Model):
    __tablename__ = "favorite_recipes"
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.String(60), db.ForeignKey('recipes.id'), primary_key=True)
