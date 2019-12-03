from google.appengine.ext import db


class Treasure(db.Model):
    lat = db.FloatProperty(required=True)
    lon = db.FloatProperty(required=True)
    description = db.StringProperty(default="")
