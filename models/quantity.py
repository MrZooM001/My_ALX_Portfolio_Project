#!/usr/bin/python3
from .base_model import BaseModel
from extensions import db

class Quantity(BaseModel, db.Model):
    __tablename__ = 'quantities'
    amount = db.Column(db.Float(), nullable=False)

    def __repr__(self):
        return "<Ingredient Quantity {}>".format(self.amount)
