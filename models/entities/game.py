from google.appengine.ext import db
from models.entities.user import User
from models.entities.zone import Zone
from models.entities.treasure import Treasure


class Game(db.Model):
    name = db.StringProperty(required=True)
    is_active = db.BooleanProperty(default=True)
    winner = db.ReferenceProperty(User, collection_name="won_games")
    zone = db.ReferenceProperty(Zone, collection_name="game", required=True)
    treasures = db.ReferenceProperty(Treasure, collection_name="game", required=True)
    owner = db.ReferenceProperty(User, collection_name="created_games", required=True)
    participants = db.ReferenceProperty(User, collection_name="participating_games")
