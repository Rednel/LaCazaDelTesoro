from google.appengine.ext import db
from models.entities.game import Game

class Treasure(db.Model):
    lat = db.IntegerProperty(required=True)
    lon = db.IntegerProperty(required=True)
    description = db.StringProperty(default="")
    game = db.ReferenceProperty(Game, collection_name="treasures", required=True)