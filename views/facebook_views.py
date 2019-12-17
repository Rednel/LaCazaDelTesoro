import os
from flask_dance.contrib.facebook import make_facebook_blueprint
from flask_dance.contrib.facebook import facebook as facebook_dance
from flask import session, redirect, url_for, Blueprint
import facebook
from models import facade
from models.entities.game import Game

from views.google_views import login_required

FACEBOOK_OAUTH_KEY = os.getenv("FACEBOOK_OAUTH_KEY")
FACEBOOK_OAUTH_SECRET = os.getenv("FACEBOOK_OAUTH_SECRET")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN")

facebook_view = Blueprint('facebook_login', __name__)

facebook_bp = make_facebook_blueprint(
    client_id=FACEBOOK_OAUTH_KEY, client_secret=FACEBOOK_OAUTH_SECRET,
    redirect_to='facebook_login.log_in_facebook')

graph = facebook.GraphAPI(access_token=FACEBOOK_ACCESS_TOKEN)


@facebook_view.route("/login")
@login_required
def log_in_facebook(user):
    if not facebook_dance.authorized:
        return redirect(url_for("facebook.login"))
    json = facebook_dance.get("/me").json()
    facade.set_user_facebook_tag(user, json.get('name'), json.get('id'))
    return redirect(url_for("profile.profile"))


@facebook_view.route("/logout")
@login_required
def log_out_facebook(user):
    session.pop('facebook_oauth_token', None)
    facade.delete_facebook_tag(user)
    return redirect(url_for("profile.profile"))


def send_facebook_message_init(game=None):
    if game is None:
        return
    message = "The new game of @[{creator_tag_id}] is open!! Search it for his creator \"{name}\"" \
              " or by the game name \"{game_name}\"".format(creator_tag_id=game.owner.facebook_tag_id,
                                                            game_name=game.name, name=game.owner.name)
    return graph.put_object("me", "feed", message=message)


def send_facebook_message_finished(game=None):
    if game.owner.facebook_tag is None and game.winner.facebook_tag is None:
        return
    if game.winner.facebook_tag is None:
        message = "The last game {game_name} of @[{creator}] finished. Congratulations to the winner :)".\
            format(creator=game.owner.facebook_tag_id, game_name=game.name)
    elif game.owner.facebook_tag is None:
        message = "Congratulations to @[{winner}] for the win in {game_name} :)".\
            format(winner=game.winner.facebook_tag_id, game_name=game.name)
    else:
        message = "The last game {game_name} of @[{creator}] finished. Congratulations to @[{winner}] :)".\
            format(winner=game.winner.facebook_tag_id, creator=game.owner.facebook_tag_id, game_name=game.name)
    return graph.put_object("me", "feed", message=message)
