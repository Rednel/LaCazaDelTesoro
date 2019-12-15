from google.appengine.ext import db

from models.entities.game import Game
from models.entities.treasure import Treasure
from models.entities.snapshot import Snapshot
from models.entities.user import User
from models.entities.participant import Participant


def owning_game(element, user):
    return element.owner.key() == user.key()


def get_created_games_by_user(user=None):
    """

    :return: all games in the database that were created by the provided user
    """
    if user is not None:
        return filter(lambda x: owning_game(element=x, user=user), Game.all())
    return list()


def get_games_not_joined_by_user(user=None):
    """

    :return: all games in the database that are actives and the user hasn't joined yet
    """
    if user is not None:
        result = list()
        for game in Game.all():
            if game not in get_active_games_by_user(user=user) and game not in get_created_games_by_user(
                    user=user) and game not in get_completed_games_by_user(user=user):
                result.append(game)
        return result
    return list()


def get_active_games_by_user(user=None):
    """

    :return: all games in the database that are associated to the user and are not completed yet
    """
    if user is not None:
        result = list()
        for participant in Participant.all():
            if participant.user.key() == user.key() and participant.game.is_active:
                result.append(participant.game)
        return result
    return list()


def get_completed_games_by_user(user=None):
    """

    :return: all games in the database that are associated to the user and are already completed
    """
    if user is not None:
        result = list()
        for participant in Participant.all():
            if participant.user.key() == user.key() and not participant.game.is_active:
                result.append(participant.game)
        return result
    return list()


def get_game_by_id(game_id=None):
    """

    :return: Game by id
    """
    if game_id is not None:
        return Game.get(game_id)
    return list()


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
                              treasures=treasures, owner=owner, participants=None, winner=None)
    return game


def delete_game(game_id=None, user=None):
    """Delete the game from db

        Args:
            :param game_id: The game id which is going to be deleted from db
                :type: Game
    """
    if user is not None and game_id is not None:
        game = Game.get(game_id)
        if game.owner.key() == user.key():
            db.delete(game.treasures)
            db.delete(game)


def join_game(game_id=None, user=None):
    """

    :param game_id: idof the game that user joins
    :param user: user what joins the game
    """

    if user is not None and game_id is not None:
        game = Game.get(game_id)
        Participant.get_or_insert(key_name=user.email + "_" + game_id, game=game, user=user)


def unjoin_game(game_id=None, user=None):
    """

    :param game_id: idof the game that user joins
    :param user: user what joins the game
    """

    if user is not None and game_id is not None:
        participant = Participant.get_or_insert(key_name=user.email + "_" + game_id)
        db.delete(participant)


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


def create_treasure(game=None, user=None, lat=None, lon=None, description=None):
    """
    Create and returns a treasure if doesnt exists one in the db with the latitude and longitude provided.
    If it exists just returns the treasure.
    :param lat(double): latitude
    :param lon(double): longitude
    :param description(string): treasure description, optional
    :param game(Game): game owner of the treasure
    :return: Treasure
    """
    if lat is not None and lon is not None and user is not None and user.key() == game.owner.key():
        return Treasure.get_or_insert(key_name=str(lat) + '_' + str(lon), lat=lat, lon=lon, description=description,
                                      game=game)
    else:
        return None


def get_all_treasures_by_game(game=None):
    """
    :param game(Game): game owner of the treasures
    :return: all treasures in the database
    """
    if game is not None:
        return game.treasures
    return list()


def delete_treasure(user=None, treasure=None):
    """
    Removes a treasure.
    :param treasure: treasure to remove
    :raise: TransactionFailedError: if the data could not be committed.
    """
    if user is not None and treasure is not None and user.key() == treasure.game.owner.key():
        db.delete(treasure)


def update_treasure(treasure=None):
    """
    Updates a treasure
    :param treasure(Treasure): treasure to update
    """
    Treasure.save(treasure)


def get_treasure_by_id(treasure_id=None):
    """
    Gets treasure related with provided id
    :param treasure_id(String): id of the treasure to get
    :return treasure(Treasure)
    """
    return Treasure.get(treasure_id)


def update_treasure_image(user=None, treasure_id=None, img=None):
    """
    Gets treasure related with provided id
    :param treasure_id(String): id of the treasure to get
    :return treasure(Treasure)
    """
    treasure = get_treasure_by_id(treasure_id)
    create_snapshot(user, treasure, img)


def create_snapshot(user=None, treasure=None, img=None):
    """
    Creates a new snapshot based in a user, treasure and image
    :param user: User that makes the snapshot
    :param treasure: Treasure related with the snapshot
    :param img: Image of the snapshot
    :return: Snapshot in case that all parameters are provided. Otherwise its returns a None
    """
    if user is not None and treasure is not None and img is not None:
        if get_snapshot_by_user_treasure is not None:
            delete_snapshot(user=user, treasure=treasure)
        return Snapshot.get_or_insert(key_name=user.email + '_' + str(treasure.key()), user=user,
                                      treasure=treasure, img=str(img))
    else:
        return None


def delete_snapshot(user=None, treasure=None):
    """
    Removes a snapshot.
    :param user: User that made the snapshot
    :param treasure: Treasure related with the snapshot to delete
    :raise: TransactionFailedError: if the data could not be committed.
    """
    if user is not None and treasure is not None:
        snapshot = get_snapshot_by_user_treasure(user=user, treasure=treasure)
        db.delete(snapshot)


def get_snapshot_by_user_treasure_in_base_64(user=None, treasure=None):
    """
    Returns a snapshot based in a user and treasure in base 64
    :param user: User that made the snapshot
    :param treasure: Treasure related with the snapshot
    :return: Snapshot in case that all parameters are provided. Otherwise its returns a None
    """
    if user is not None and treasure is not None:
        for snapshot in Snapshot.all():
            if snapshot.treasure.key() == treasure.key() and snapshot.user.key() == user.key():
                return snapshot.img.encode('base64')
    return None


def get_snapshot_by_user_treasure(user=None, treasure=None):
    """
    Returns a snapshot based in a user and treasure
    :param user: User that made the snapshot
    :param treasure: Treasure related with the snapshot
    :return: Snapshot in case that all parameters are provided. Otherwise its returns a None
    """
    if user is not None and treasure is not None:
        for snapshot in Snapshot.all():
            if snapshot.treasure.key() == treasure.key() and snapshot.user.key() == user.key():
                return snapshot
    return None


def get_all_user():
    return User.all()


def get_or_insert_user(email=None, name=None, surname="", picture=None):
    if name is None or email is None or picture is None:
        return None
    user = User.get_or_insert(key_name=email, email=email, name=name, surname=surname, picture=picture)
    return user
