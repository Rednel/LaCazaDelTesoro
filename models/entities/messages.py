from google.appengine.ext import db
from models.entities.user import User
from models.entities.conversation import Conversation

class Message(db.Model):
    user = db.ReferenceProperty(User, collection_name="message", required=True)
    message = db.StringProperty(required=True)
    time = db.DateTimeProperty(auto_now=True)
    conversation = db.ReferenceProperty(Conversation, collection_name="conversation", required=True)