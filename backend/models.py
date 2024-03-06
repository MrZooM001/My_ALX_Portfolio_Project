from extentions import db
from base_model import BaseModel

class Recipe(BaseModel, db.Model):
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


"""
User:
    id: uuid
    username: string
    email: string
    password: string
"""
class User(BaseModel, db.Model):
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.Text(), nullable=False)

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
