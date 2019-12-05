from google.appengine.ext import db


class Zone(db.Model):
    latitude = db.StringProperty(required=True)
    longitude = db.StringProperty(required=True)
    height = db.StringProperty()
    width = db.StringProperty()
    # game = db.ReferenceProperty(Zone, collection_name="zone", required=True)

