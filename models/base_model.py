#!/usr/bin/python3
from extensions import db
from datetime import datetime
from uuid import uuid4

time_format = "%Y-%m-%dT%H:%M:%S.%f"


class BaseModel():
    """
    a base model for all models
    """
    id = db.Column(db.String(60), primary_key=True)
    created_at = db.Column(db.DateTime(), default=datetime.now)
    updated_at = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    def __init__(self, *args, **kwargs):
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time_format)
            else:
                self.created_at = datetime.now()
            
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time_format)
            else:
                self.updated_at = datetime.now()

            if kwargs.get("id", None) is None:
                self.id = str(uuid4())
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
