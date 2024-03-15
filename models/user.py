#!/usr/bin/python3
from flask_login import UserMixin
from .base_model import BaseModel
from extensions import db

class User(BaseModel, db.Model, UserMixin):
    __tablename__ = 'users'
    username = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(90), nullable=False, unique=True)
    password = db.Column(db.String(90), nullable=False)
    first_name = db.Column(db.String(60), nullable=True)
    last_name = db.Column(db.String(60), nullable=True)
    profile_image = db.Column(db.Text(), nullable=True)

    recipes = db.relationship("UserFavorite", back_populates="users")

    def __init__(self, username=None, email=None, password=None, *args, **kwds):
        super().__init__(*args, **kwds)
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return "<User {}>".format(self.username)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

