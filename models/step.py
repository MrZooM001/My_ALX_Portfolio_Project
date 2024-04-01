#!/usr/bin/python3
"""
Module defines the Step class, which represents a single step in a recipe.
"""
from .base_model import BaseModel
from extensions import db

class Step(BaseModel, db.Model):
    """
    This class represents a single step in a recipe.
    
    Args:
        db (SQLAlchemy object): The SQLAlchemy object that is used to interact with the database.
    
    Attributes:
        instruction (str): The step's instruction.
        recipe_id (str): The recipe ID to which the step belongs.
        recipe (Recipe): The recipe object to which the step belongs.
    """
    __tablename__ = "steps"
    instruction = db.Column(db.Text(), nullable=False)

    recipe_id = db.Column(db.String(60), db.ForeignKey("recipes.id"), nullable=False)
    recipe = db.relationship("Recipe", backref=db.backref('steps', lazy='dynamic', collection_class=list))

    def __repr__(self):
        return "<Step: {}...>".format(self.instruction[:24])
