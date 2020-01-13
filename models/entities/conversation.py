from google.appengine.ext import db
from models.entities.user import User


class Conversation(db.Model):
    user1 = db.ReferenceProperty(User, required=True, collection_name="conversation1")
    user2 = db.ReferenceProperty(User, required=True, collection_name="conversation2")
    message = db.StringProperty()
