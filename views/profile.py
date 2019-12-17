from flask import session, redirect, url_for, Blueprint, abort, render_template
import requests

from views.google_views import login_required

profile_view = Blueprint('profile', __name__)


@profile_view.route("/")
@login_required
def profile(user):
    return render_template("user_profile.html", user=user)

