#!/usr/bin/python3
"""
Module defines the database schema for the users table.
"""
from flask_login import UserMixin
from .base_model import BaseModel
from extensions import db
from enum import Enum


class Gender(Enum):
    """
    Class as an enumeration that defines the possible genders.
    """
    Female = 1
    Male = 2

class User(BaseModel, db.Model, UserMixin):
    """
    Class defines the database schema for the user model.
    
    Args:
        db (SQLAlchemy object): The SQLAlchemy object that is used to interact with the database.
        UserMixin (class): Provides default implementations for the methods that Flask-Login expects user objects to have

    Attributes:
        username (str): The username of the user
        email (str): The email of the user
        password (str): The password of the user
        first_name (str): The first name of the user
        last_name (str): The last name of the user
        profile_img (str): The profile image of the user
        is_admin (bool): A flag indicating whether the user is an administrator
        gender (Gender): The gender of the user
        favorites (list): A list of recipes that the user has marked as favorites
    """
    __tablename__ = "users"
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    profile_img = db.Column(db.Text(), nullable=True)
    is_admin = db.Column(db.Boolean(), default=False)
    gender = db.Column(db.Enum(Gender, name="Gender"), default= Gender.Female)

    favorites = db.relationship(
        "Recipe",
        secondary="favorite_recipes",
        backref=db.backref("favorite_by", lazy="dynamic", collection_class=list),
    )

    def __init__(self, username=None, email=None, password=None, *args, **kwds):
        super().__init__(*args, **kwds)
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User {}>".format(self.username)

    def save(self):
        """Saves the user to the database"""
        db.session.add(self)
        db.session.commit()
