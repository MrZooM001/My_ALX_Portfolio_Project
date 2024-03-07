#!/usr/bin/python3
from models.base_model import BaseModel
from api.v1.extentions import db

class User(BaseModel, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)

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
