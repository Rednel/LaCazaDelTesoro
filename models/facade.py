from google.appengine.ext import db

from models.entities.treasure import Treasure
from models.entities.snapshot import Snapshot
from models.entities.game import Game
from models.entities.user import User
from models.entities.zone import Zone


def get_or_insert_game(zone=None, treasures=None, owner=None, name=None, is_active=True):
    """Get or insert the game with the information provided

        Args:
            :param is_active: Allows knowing if the game is active or not.
                :type: Boolean
            :param name: The name that receives the game.
                :type: String
            :param owner: The user who is the owner of the game
                :type: User
            :param treasures: The list of treasures the participants need to find to win the game
                :type: [Treasure]
            :param zone: The zone where the treasures are located
                :type: Zone
        Raises:
            Exception: if the required parameters are not present or are None
        Returns:
            Game: The game from db or the one which was just created
    """
    if name is None or owner is None or owner.email is None:
        return None
    game = Game.get_or_insert(key_name=owner.email + "_" + name, is_active=is_active, name=name, zone=zone,
                              treasures=treasures, owner=owner, participants=[], winner=None)
    return game


def delete_game(game=None):
    """Delete the game from db

        Args:
            :param game: The game which is going to be deleted from db
                :type: Game
    """
    db.delete(game)


def get_game_by_owner_and_name(owner=None, game_name=None):
    """Get the game from db whose name is "game_name" and the owner is "owner"
        Args:
            :param owner: The owner of the game to obtain
                :type: User
            :param game_name: The name of the game to obtain
                :type: String
    """
    if owner is None or owner.email is None or game_name is None:
        return None
    return Game.get_by_key_name(key_names=owner.email + "_" + game_name)


def get_game_by_id(_id=None):
    """Get the game from db with the id provided
        Args:
            :param _id: The id of the game to search in db
                :type: Game
        Returns:
            Game: The game if it is already stored, None in other case
    """
    if _id is None:
        return None
    return Game.get_by_id(ids=_id)


def exists_game(game=None):
    """Get a boolean value corresponding with the evidence of an existing game provided in db
        Args:
            :param game: The game to search in db
                :type: Game
        Returns:
            Boolean: Specify if the game is already stored in db
    """
    if game is None or game.name is None or game.owner is None or game.owner.email is None:
        return False
    return Game.get_by_key_name(key_names=game.owner.email + "_" + game.name) is not None


def get_all_user():
    return User.all()


def set_user_twitter_tag(user, tag):
    user.twitter_tag = tag
    user.put()


def delete_twitter_tag(user):
    user.twitter_tag = None
    user.put()


def set_user_facebook_tag(user, tag, _id):
    user.facebook_tag = tag
    user.facebook_tag_id = _id
    user.put()


def delete_facebook_tag(user):
    user.facebook_tag = None
    user.facebook_tag_id = None
    user.put()


def get_or_insert_user(email=None, name=None, surname="", picture=None):
    if name is None or email is None or picture is None:
        return None
    user = User.get_or_insert(key_name=email, email=email, name=name, surname=surname, picture=picture)
    return user


def create_treasure(lat=None, lon=None, text=None, game=None):
    """
    Create and returns a treasure if doesnt exists one in the db with the latitude and longitude provided.
    If it exists just returns the treasure.
    :param lat(double): lattitude
    :param lon(double): longitude
    :param text(string): treasure description, optional
    :param game(Game): game owner of the treasure
    :return: Treasure
    """
    if lat is not None and lon is not None:
        return Treasure.get_or_insert(key_name=lat + '_' + lon, lat=lat, lon=lon, text=text, game=game)
    else:
        return None


def remove_treasure(treasure=None):
    """
    Removes a treasure.
    :param treasure(Treasure): treasure to remove
    :raise: TransactionFailedError: if the data could not be committed.
    """
    db.delete(treasure)


def update_treasure(treasure=None):
    """
    Updates a treasure
    :param treasure(Treasure): treasure to update
    """
    Treasure.save(treasure)


def create_snapshot(user=None, treasure=None, img=None):
    """
    Creates a new snapshot based in a user, treasure and image
    :param user: User that makes the snapshot
    :param treasure: Treasure related with the snapshot
    :param img: Image of the snapshot
    :return: Snapshot in case that all parameters are provided. Otherwise its returns a None
    """
    if user is not None and treasure is not None and img is not None:
        return Snapshot.get_or_insert(key_name=user.email + '_' + treasure.lat + '_' + treasure.lon, user=user,
                                      treasure=treasure, img=img)
    else:
        return None


def remove_snapshot(snapshot=None):
    """
    Removes a snapshot.
    :param snapshot(Snapshot): snapshot to remove
    :raise: TransactionFailedError: if the data could not be committed.
    """
    db.delete(snapshot)


def update_snapshot(snapshot=None):
    """
    Updates a snapshot.
    :param snapshot(Snapshot): snapshot to update
    """
    Snapshot.save(snapshot)


""" 
CRUD User       
"""


def user_all():
    data = User.all()
    return data


#  get user info
def get_user_one(id):
    user = db.get(db.Key.from_path('User', id))
    return user


#  new user
def insert_user_new(email, name, surname, picture):
    user = User(
        email=str(email),
        name=str(name),
        surname=str(surname),
        picture=str(picture),
    )
    user.put()


def user_update_model(id, name, email, surname, picture):
    user_id = int(id)
    user = db.get(db.Key.from_path('User', user_id))
    user.email = email
    user.name = name
    user.surname = surname
    user.picture = picture
    user.put()

#  delete user
def user_delete_model(id):
    if id:
        user = db.get(db.Key.from_path('User', id))
        db.delete(user)


""" 
CRUD Zone       
"""

# zone list
def get_zone_all():
    data = Zone.all()
    return data

#  get zona info
def zone_one_model(id):
    zone = db.get(db.Key.from_path('Zone', id))
    return zone

#  new zone
def insert_zone_new(name, latitude, longitude, height, width):
        zone = Zone(
            name=name,
            latitude=latitude,
            longitude=longitude,
            height=height,
            width=width,
        )
        zone.put()

#  delete edit
def zone_edit_model(id, name, latitude, longitude, height, width):
        zone_id = int(id)
        zone = db.get(db.Key.from_path('Zone', zone_id))
        zone.name = name
        zone.latitude = latitude
        zone.longitude = longitude
        zone.height = height
        zone.width = width
        zone.put()

#  delete zone
def zone_delete_model(id):
    if id:
        zone = db.get(db.Key.from_path('Zone', id))
        db.delete(zone)


"""
SEARCH FOR GAME
"""

def game_search(keyword):
    if keyword:
        keyword = str(keyword)
        q = Game.all()
        result = q.filter("game_name =", keyword)
        return render_template('game_search.html', data=result)
