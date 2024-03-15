#!/usr/bin/python3
from .base_model import BaseModel
from extensions import db

class MeasurementUnit(BaseModel, db.Model):
    __tablename__ = 'measurement_units'
    name = db.Column(db.String(20), nullable=False, unique=True)

    def __repr__(self):
        return "<Ingredient Unit {}>".format(self.name)
