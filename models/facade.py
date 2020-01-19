from google.appengine.ext import db

from models.entities.treasure import Treasure
from models.entities.snapshot import Snapshot
from models.entities.game import Game
from models.entities.user import User
from models.entities.participant import Participant

import json


def owning_game(element, user):
    print(user.role)
    return element.owner.key() == user.key() or user.role == "admin"


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
            if (participant.user.key() == user.key()) or user.role == "admin" and participant.game.is_active:
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
            if (participant.user.key() == user.key()) or user.role == "admin" and not participant.game.is_active:
                result.append(participant.game)
        return result
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
        if game.owner.key() == user.key() or user.role == "admin":
            for treasure in game.treasures:
                db.delete(treasure.images)
                db.delete(treasure)
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

    :param game_id: id of the game that user joins
    :param user: user what joins the game
    """

    if user is not None and game_id is not None:
        game = get_game_by_id(game_id)
        for treasure in game.treasures:
            delete_snapshot(user=user, treasure=treasure)
        participant = Participant.get_or_insert(key_name=user.email + "_" + game_id)
        db.delete(participant)


def win_game(game=None, winner=None, owner=None):
    """
    Makes winner user win the game
    :param game: game that winner won
    :param winner: winner of the game
    :param owner: owner of the game
    """
    if game is not None and winner is not None and owner is not None and (
            game.owner.key() == owner.key() or owner.role == "admin"):
        game.winner = winner
        game.is_active = False
        Game.save(game)
        return game


def reopen_game(game=None, user=None):
    """
    Removes game winner and reopens the game
    :param game_id: id of the game to reopen
    :param user: user that reopens the game, must be the owner of the game
    """

    if game is not None and user is not None and (game.owner.key() == user.key() or user.role == "admin"):
        game.winner = None
        game.is_active = True
        for treasure in game.treasures:
            for image in treasure.images:
                Snapshot.delete(image)
        Game.save(game)


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


def get_game_by_id(game_id=None):
    """Get the game from db with the id provided
        Args:
            :param _id: The id of the game to search in db
                :type: Game
        Returns:
            Game: The game if it is already stored, None in other case
    """
    if game_id is None:
        return None
    return Game.get(game_id)


def exists_game(game_name=None, user=None):
    """Get a boolean value corresponding with the evidence of an existing game provided in db
        Args:
            :param game: The game to search in db
                :type: Game
        Returns:
            Boolean: Specify if the game is already stored in db
    """
    if game_name is None or user is None:
        return False
    return Game.get_by_key_name(key_names=user.email + "_" + game_name) is not None


def write_game_json(game=None, user=None, map_json=None):
    """
    Updates map property in game entity
    :param game: game to update
    :param user: user that made the update. Must be the owner of the game
    :param map_json: json to write in map property of game
    :return: game updated
    """
    if game is not None and user is not None and (
            user.key() == game.owner.key() or user.role == "admin") and map_json is not None:
        create_treasures_with_json(game=game, user=user, map_json=json.loads(map_json))
        print(map_json)
        game.map = json.dumps(map_json)
        return Game.put(game)
    else:
        return None


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


def get_all_treasures_by_game(game=None):
    """
    :param game(Game): game owner of the treasures
    :return: all treasures in the database
    """
    if game is not None:
        return game.treasures
    return list()


def get_snapshots_by_game(owner=None, game=None):
    """
    Returns participant, images tuples based in a game
    :param game: Game that contains the snapshots
    :param owner: Owner of the game that is the only that can have access to the information
    :return: participant, images tuples in case that all parameters are provided. Otherwise its returns a None
    """
    result = list()
    if owner is not None and game is not None and (owner.key() == game.owner.key() or owner.role == "admin"):
        for participant in game.participants:
            images = len(filter(lambda image: image.treasure in game.treasures, participant.user.images))
            result.append((participant.user, images))
    return result


def get_snapshots_by_game_and_user(owner=None, game=None, user=None):
    """
    Returns snapshot list based in a user and game
    :param game: Game that contains the snapshots
    :param owner: Owner of the game that is the only that can have access to the information
    :param user: User provided to filter snapshots
    :return: snapshot list in case that all parameters are provided. Otherwise its returns a None
    """
    result = list()
    if owner is not None and game is not None and owner.key() == game.owner.key() and user is not None and game in get_active_games_by_user(
            user=user):
        images = filter(lambda image: image.treasure in game.treasures, user.images)
        for image in images:
            result.append((image, image.img.encode('base64')))
    return result


def get_all_user():
    return User.all()


def get_user_by_user_id(user_id=None):
    """
    Returns a user based in a user_id
    :param user_id: Id of the user to return
    :return: User in case that all parameters are provided. Otherwise its returns a None
    """
    if user_id is not None:
        return User.get(user_id)
    return list()


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


def create_treasures_with_json(game=None, user=None, map_json=None):
    """
    Creates treasures and zones using a geo json
    :param game: game where create treasures
    :param user: user that creates the treasures. Must be the owner of the game.
    :param map_json: geo_json that contains map data
    :return: None
    """

    if game is not None and map_json is not None and user is not None:
        delete_all_game_treasures(game=game, user=user)
        for feature in map_json.get('features'):
            feature_type = feature.get('geometry').get('type')
            if feature_type == "Polygon":
                print("create_zone")
            elif feature_type == "Point":
                if feature.get('geometry').get('coordinates') is not None and feature.get('properties').get(
                        'name') is not None:
                    latitude = feature.get('geometry').get('coordinates')[0]
                    longitude = feature.get('geometry').get('coordinates')[1]
                    name = feature.get('properties').get('name')
                    create_treasure(game=game, user=user, name=name, lat=latitude, lon=longitude)


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


def create_treasure(game=None, user=None, name=None, lat=None, lon=None, description=None):
    """
    Create and returns a treasure if doesnt exists one in the db with the latitude and longitude provided.
    If it exists just returns the treasure.
    :param name(string): treasure name
    :param lat(double): latitude
    :param lon(double): longitude
    :param description(string): treasure description, optional
    :param game(Game): game owner of the treasure
    :return: Treasure
    """
    if name is not None and lat is not None and lon is not None and user is not None and (
            user.key() == game.owner.key() or user.role == "admin"):
        return Treasure.get_or_insert(key_name=name + '_' + str(lat) + '_' + str(lon), lat=lat, lon=lon,
                                      name=name,
                                      description=description,
                                      game=game)
    else:
        return None


def delete_all_game_treasures(user=None, game=None):
    """
        Removes all treasures of the game. The user provided must be owner of the game
        :param game: game to eliminate treasures
        :raise: TransactionFailedError: if the data could not be committed.
        """
    if user is not None and game is not None and (user.key() == game.owner.key() or user.role == "admin"):
        db.delete(game.treasures)


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


def create_snapshot(user=None, treasure=None, img=None):
    """
    Creates a new snapshot based in a user, treasure and image
    :param user: User that makes the snapshot
    :param treasure: Treasure related with the snapshot
    :param img: Image of the snapshot
    :return: Snapshot in case that all parameters are provided. Otherwise its returns a None
    """
    if user is not None and treasure is not None and img is not None:
        image = db.Blob(img)
        if get_snapshot_by_user_treasure(user=user, treasure=treasure) is not None:
            delete_snapshot(user=user, treasure=treasure)
        return Snapshot.get_or_insert(key_name=user.email + '_' + str(treasure.key()), user=user,
                                      treasure=treasure, img=image)
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
        if snapshot is not None:
            db.delete(snapshot)


def delete_snapshot_by_admin(admin=None, user=None, treasure=None):
    """
    Removes a snapshot as admin of the game.
    :param admin: User that owns the game where the snapshot was uploaded.
    :param user: User that made the snapshot.
    :param treasure: Treasure related with the snapshot to delete
    :raise: TransactionFailedError: if the data could not be committed.
    """
    if user is not None and treasure is not None and admin is not None:
        if treasure.game.owner.key() == admin.key() or admin.role == "admin":
            snapshot = get_snapshot_by_user_treasure(user=user, treasure=treasure)
            db.delete(snapshot)


def get_or_insert_user(email=None, name=None, surname="", picture=None):
    if name is None or email is None or picture is None:
        return None
    user = User.get_or_insert(key_name=email, email=email, name=name, surname=surname, picture=picture)
    return user
