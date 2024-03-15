#!/usr/bin/python3
from extensions import db

class UserFavorite(db.Model):
    __tablename__ = "user_favorites"
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), primary_key=True)
    recipe_id = db.Column(db.String(60), db.ForeignKey('recipes.id'), primary_key=True)
    favorite = db.Column(db.Boolean(), nullable=False, default=False)

    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'recipe_id'),)

    users = db.relationship("User", back_populates="recipes")

    recipes = db.relationship("Recipe", back_populates="users")
