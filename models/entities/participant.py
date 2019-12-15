from google.appengine.ext import db
from models.entities.game import Game
from models.entities.user import User


class Participant(db.Model):
    game = db.ReferenceProperty(Game, collection_name="participants", required=True)
    user = db.ReferenceProperty(User, collection_name="games", required=True)