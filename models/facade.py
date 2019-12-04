from google.appengine.ext import db

from models.entities.game import Game
from models.entities.treasure import Treasure
from models.entities.snapshot import Snapshot


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


def create_treasure(lat=None, lon=None, description=None, game=None):
    """
    Create and returns a treasure if doesnt exists one in the db with the latitude and longitude provided.
    If it exists just returns the treasure.
    :param lat(double): lattitude
    :param lon(double): longitude
    :param description(string): treasure description, optional
    :param game(Game): game owner of the treasure
    :return: Treasure
    """
    if lat is not None and lon is not None:
        return Treasure.get_or_insert(key_name=str(lat) + '_' + str(lon), lat=lat, lon=lon, description=description, game=game)
    else:
        return None


def get_treasures():
    """

    :return: all treasures in the database
    """
    return Treasure.all()


def remove_treasure(treasure_id=None):
    """
    Removes a treasure.
    :param treasure_id: treasure id to remove
    :raise: TransactionFailedError: if the data could not be committed.
    """
    treasure_to_delete = db.get(db.Key.from_path('Treasure', treasure_id))
    db.delete(treasure_to_delete)


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
