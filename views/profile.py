from flask import Blueprint, render_template

from views.google_views import login_required

profile_view = Blueprint('profile', __name__)


@profile_view.route("/")
@login_required
def profile(user):
    return render_template("user_profile.html", user=user)

