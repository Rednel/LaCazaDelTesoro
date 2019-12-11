from google.appengine.ext import db
from models.entities.user import User
from models.entities.zone import Zone


class Game(db.Model):
    name = db.StringProperty(required=True)
    is_active = db.BooleanProperty(default=True)
    winner = db.ReferenceProperty(User, collection_name="won_games")
    zone = db.ReferenceProperty(Zone, collection_name="game")
    owner = db.ReferenceProperty(User, collection_name="created_games", required=True)
    participants = db.ReferenceProperty(User, collection_name="participating_games")
