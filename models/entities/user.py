from google.appengine.ext import db


class User(db.Model):
    email = db.StringProperty(required=True)
    user_name = db.StringProperty(required=True)
    first_name = db.StringProperty()
    last_name = db.StringProperty()
    gender = db.StringProperty()
    date_of_birth = db.DateProperty(auto_now=True)
    role = db.StringProperty()
    createdAt = db.DateTimeProperty(auto_now=True)
