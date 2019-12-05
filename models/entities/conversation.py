from google.appengine.ext import db
from models.entities.user import User

class Conversation(db.Model):
    user = db.ReferenceProperty(User, collection_name="conversation_user", required=True)