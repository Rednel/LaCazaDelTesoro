from google.appengine.ext import db
from models.entities.user import User
from models.entities.conversation import Conversation


class Message(db.Model):
    user = db.ReferenceProperty(User, required=True, collection_name="messages")
    message = db.StringProperty(required=True)
    time = db.DateTimeProperty(auto_now_add=True)
    conversation = db.ReferenceProperty(Conversation, required=True, collection_name="messages")
