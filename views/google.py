import os
from flask_dance.contrib.google import make_google_blueprint, google
from flask import session, redirect, url_for, Blueprint, abort
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
import requests

from models.facade import get_or_insert_user
from functools import wraps

GOOGLE_OAUTH_ID = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
GOOGLE_OAUTH_SECRET = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")

google_view = Blueprint('google_login', __name__)

google_scopes = [
    'openid',
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

google_bp = make_google_blueprint(
    client_id=GOOGLE_OAUTH_ID, client_secret=GOOGLE_OAUTH_SECRET,
    scope=google_scopes, redirect_to='google_login.log_in_google',
    reprompt_select_account=True)


@google_view.route("/login")
def log_in_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    json = google.get("/oauth2/v2/userinfo").json()
    user = get_or_insert_user(email=json['email'], name=json['given_name'],
                              surname=json['family_name'], picture=json['picture'])
    session['user'] = user
    return redirect(url_for("home"))


@google_view.route("/logout")
def log_out_google():
    session.clear()
    return redirect(url_for("home"))


def login_required(function):
    @wraps(function)
    def wrap(*args, **kwargs):
        if not google.authorized:
            return redirect(url_for("google.login"))
        try:
            json = google.get('/oauth2/v2/userinfo').json()
            user = get_or_insert_user(email=json['email'], name=json['given_name'],
                                      surname=json['family_name'], picture=json['picture'])
            return function(user, *args, **kwargs)
        except TokenExpiredError:
            return redirect(url_for("google.login"))
        except requests.RequestException:
            abort(500)
    return wrap
