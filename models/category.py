from .base_model import BaseModel
from extensions import db


class Category(BaseModel, db.Model):
    __tablename__ = "categories"
    name = db.Column(db.String(60), nullable=False, unique=True)


    def __repr__(self):
        return "<Category {}>".format(self.name)
