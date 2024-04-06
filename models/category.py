#!/usr/bin/python3
"""
Module defines the database schema for the categories table.
"""
from .base_model import BaseModel
from extensions import db


class Category(BaseModel, db.Model):
    """
    Class represents a category in the database.
    """
    __tablename__ = "categories"
    name = db.Column(db.String(60), nullable=False, unique=True)


    def __repr__(self):
        return "<Category {}>".format(self.name)
    
    def get_all():
        """
        Function as helper method that retrieves a list of categories.

        Returns:
            A list of Category objects.
        """
        categories = Category.query.order_by(Category.name).all()
        return categories
