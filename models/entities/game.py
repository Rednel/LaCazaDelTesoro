from google.appengine.ext import db
from models.entities.user import User
from models.entities.zone import Zone


class Game(db.Model):
    name = db.StringProperty(required=True)
    is_active = db.BooleanProperty(required=True)
    winner = db.ReferenceProperty(User, collection_name="won_games")
    zone = db.ReferenceProperty(Zone, collection_name="game")
    owner = db.ReferenceProperty(User, collection_name="created_games", required=True)

    def __eq__(self, other):
        return isinstance(other, Game) and other.key() == self.key()
