from google.appengine.ext import db
from json import JSONEncoder


class User(db.Model, JSONEncoder):
    email = db.StringProperty(required=True)
    name = db.StringProperty(required=True)
    surname = db.StringProperty(required=True)
    picture = db.StringProperty(required=True)
    role = db.StringProperty(default="user")
    twitter_tag = db.StringProperty(default=None)
    facebook_tag = db.StringProperty(default=None)
    facebook_tag_id = db.StringProperty(default=None)

    def default(self, o):
        return {"email": o.email,
                "name": o.name,
                "surname": o.surname,
                "picture": o.picture,
                "role": o.role}

    def __eq__(self, other):
        return isinstance(other, User) and other.key() == self.key()

    JSONEncoder.default = default
