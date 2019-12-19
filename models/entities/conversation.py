from google.appengine.ext import db

class Conversation(db.Model):
    user1 = db.IntegerProperty()
    user2 = db.IntegerProperty()