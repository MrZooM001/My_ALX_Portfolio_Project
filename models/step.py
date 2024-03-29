#!/usr/bin/python3
from .base_model import BaseModel
from extensions import db

class Step(BaseModel, db.Model):
    __tablename__ = "steps"
    instruction = db.Column(db.Text(), nullable=False)

    recipe_id = db.Column(db.String(60), db.ForeignKey("recipes.id"), nullable=False)
    recipe = db.relationship("Recipe", backref=db.backref('steps', lazy='dynamic', collection_class=list))

    def __repr__(self):
        return "<Step: {}...>".format(self.instruction[:24])
