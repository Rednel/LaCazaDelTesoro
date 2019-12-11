from google.appengine.ext import db
from models.entities.game import Game


class Treasure(db.Model):
    lat = db.FloatProperty(required=True)
    lon = db.FloatProperty(required=True)
    description = db.StringProperty(default="")
    game = db.ReferenceProperty(Game, collection_name="treasures")
