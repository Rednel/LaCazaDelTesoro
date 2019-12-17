import os
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_dance.contrib.twitter import twitter as twitter_dance
from flask import session, redirect, url_for, Blueprint
import twitter
from models import facade

from views.google_views import login_required

TWITTER_OAUTH_KEY = os.getenv("TWITTER_OAUTH_KEY")
TWITTER_OAUTH_SECRET = os.getenv("TWITTER_OAUTH_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

twitter_view = Blueprint('twitter_login', __name__)

twitter_bp = make_twitter_blueprint(
    api_key=TWITTER_OAUTH_KEY, api_secret=TWITTER_OAUTH_SECRET,
    redirect_to='twitter_login.log_in_twitter')

api = twitter.Twitter(auth=twitter.OAuth(consumer_key=TWITTER_OAUTH_KEY, consumer_secret=TWITTER_OAUTH_SECRET,
                                         token=TWITTER_ACCESS_TOKEN, token_secret=TWITTER_ACCESS_TOKEN_SECRET))


@twitter_view.route("/login")
@login_required
def log_in_twitter(user):
    if not twitter_dance.authorized:
        return redirect(url_for("twitter.login"))
    tag = "@" + twitter_dance.get("account/settings.json").json()['screen_name']
    facade.set_user_twitter_tag(user, tag)
    return redirect(url_for('profile.profile'))


@twitter_view.route("/logout")
@login_required
def log_out_twitter(user):
    session.pop('twitter_oauth_token', None)
    facade.delete_twitter_tag(user)
    return redirect(url_for('profile.profile'))


def send_twitter_message_init(game=None):
    if game is None:
        return
    message = "The new game of {creator_tag} is open!! Search it for his creator \"{name}\"" \
              " or by the game name \"{game_name}\"".format(creator_tag=game.owner.twitter_tag, game_name=game.name,
                                                            name=game.owner.name)
    return api.statuses.update(status=message)


def send_twitter_message_finished(game=None):
    if game.owner.twitter_tag is None and game.winner.twitter_tag is None:
        return
    if game.winner.twitter_tag is None:
        message = "The last game {game_name} of {creator} finished. Congratulations to the winner :)".\
            format(creator=game.owner.twitter_tag, game_name=game.name)
    elif game.owner.twitter_tag is None:
        message = "Congratulations to {winner} for the win in {game_name} :)".\
            format(winner=game.winner.twitter_tag, game_name=game.name)
    else:
        message = "The last game {game_name} of {creator} finished. Congratulations to {winner} :)".\
            format(winner=game.winner.twitter_tag, creator=game.owner.twitter_tag, game_name=game.name)
    return api.statuses.update(status=message)
