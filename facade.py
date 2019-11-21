from models import Treasure, Snapshot
from google.appengine.ext import db


def create_treasure(lat=None, lon=None, text=None, game=None):
    if lat is not None and lon is not None:
        return Treasure.get_or_insert(key_name=lat + '_' + lon, lat=lat, lon=lon, text=text, game=game)
    else:
        return None


def remove_treasure(treasure=None):
    return db.delete(treasure)


def update_treasure(treasure=None):
    return Treasure.save(treasure)


def create_snapshot(user=None, treasure=None, img=None):
    if user is not None and treasure is not None and img is not None:
        return Snapshot.get_or_insert(key_name=user.email + '_' + treasure.lat + '_' + treasure.lon, user=user, treasure=treasure, img=img)
    else:
        return None


def remove_snapshot(snapshot=None):
    return db.delete(snapshot)


def update_snapshot(snapshot=None):
    return Snapshot.save(snapshot)

