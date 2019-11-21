from google.appengine.ext import db


class Game(db.Model):
    pass


class User(db.Model):
    email = db.StringProperty(required=True)
    pass


class Treasure(db.Model):
    lat = db.IntegerProperty(required=True)
    lon = db.IntegerProperty(required=True)
    description = db.StringProperty(default="")
    game = db.ReferenceProperty(Game, collection_name="treasures", required=True)


class Snapshot(db.Model):
    img = db.BlobProperty(required=True)
    treasure = db.ReferenceProperty(Treasure, collection_name="images", required=True)
    user = db.ReferenceProperty(User, collection_name="images", required=True)