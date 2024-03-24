#!/usr/bin/python3
from flask_login import UserMixin
from .base_model import BaseModel
from extensions import db


class User(BaseModel, db.Model, UserMixin):
    __tablename__ = "users"
    username = db.Column(db.String(40), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    profile_img = db.Column(db.Text(), nullable=True)
    is_admin = db.Column(db.Boolean(), default=False)

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
        db.session.add(self)
        db.session.commit()
