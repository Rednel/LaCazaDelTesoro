from google.appengine.ext import db
from json import JSONEncoder


class User(db.Model, JSONEncoder):
    email = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    surname = db.StringProperty(required=True)
    picture = db.StringProperty(required=False)
    role = db.StringProperty(default="user")

    def default(self, o):
        return {"email": o.email,
                "name": o.name,
                "surname": o.surname,
                "picture": o.picture,
                "role": o.role}

    JSONEncoder.default = default
