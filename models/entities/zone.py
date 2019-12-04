from google.appengine.ext import db


class Zone(db.Model):
    name = db.StringProperty(required=True)