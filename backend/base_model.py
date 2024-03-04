from extentions import db
from uuid import uuid4

class BaseModel():
    id = db.Column(db.String(60), primary_key=True)
    
    def __init__(self, *args, **kwds):
        self.id = str(uuid4())
