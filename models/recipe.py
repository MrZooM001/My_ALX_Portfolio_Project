#!/usr/bin/python3
from models.base_model import BaseModel
from api.v1.extentions import db

class Recipe(BaseModel, db.Model):
    __tablename__ = "recipes"
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text(), nullable=False)
    
    def __init__(self, title=None, description=None, *args, **kwargs):
        """initializes Recipe"""
        super().__init__(*args, **kwargs)
        self.title = title
        self.description = description

    def __repr__(self):
        return "<Recipe {}>".format(self.title)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title, description):
        self.title = title
        self.description = description
        db.session.commit()

