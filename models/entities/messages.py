from google.appengine.ext import db


class Message(db.Model):
    user = db.IntegerProperty()
    message = db.StringProperty(required=True)
    time = db.StringProperty(required=True)
    conversation = db.IntegerProperty()
    orden = db.IntegerProperty()