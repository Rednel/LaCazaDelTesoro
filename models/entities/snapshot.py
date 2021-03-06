from google.appengine.ext import db
from models.entities.treasure import Treasure
from models.entities.user import User


class Snapshot(db.Model):
    treasure = db.ReferenceProperty(Treasure, collection_name="images", required=True)
    user = db.ReferenceProperty(User, collection_name="images", required=True)
    img = db.BlobProperty(required=True)
