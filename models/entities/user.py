from google.appengine.ext import db
from json import JSONEncoder
from models.entities.treasure import Treasure


class User(db.Model, JSONEncoder):
    email = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    surname = db.StringProperty(required=True)
    picture = db.StringProperty(required=True)
    role = db.StringProperty(default="user")

    def default(self, o):
        return {"email": o.email,
                "name": o.name,
                "surname": o.surname,
                "picture": o.picture,
                "role": o.role}

    JSONEncoder.default = default
