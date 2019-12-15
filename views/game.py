from flask import render_template, request, Blueprint, redirect, url_for
import models.facade
from views.google import login_required

game_view = Blueprint('game_views', __name__)


@game_view.route("/", methods=['GET'])
@login_required
def show_not_joined_games(user):
    games = models.facade.get_games_not_joined_by_user(user)
    return render_template('games.html', games=games, user=user)


@game_view.route('/add', methods=['GET'])
def render_games_form_get():
    return render_template('new_game_form.html')


@game_view.route('/add', methods=['POST'])
@login_required
def render_games_form_post(user):
    name = request.form.get('inputGameName')
    if name != "":
        models.facade.get_or_insert_game(name=name, owner=user)
        return redirect(url_for("game_views.show_created_games"))
    else:
        return render_template('new_game_form.html')


@game_view.route("/created", methods=['GET'])
@login_required
def show_created_games(user):
    games = models.facade.get_created_games_by_user(user)
    return render_template('games.html', games=games, user=user)


@game_view.route("/completed", methods=['GET'])
@login_required
def show_completed_games(user):
    games = models.facade.get_completed_games_by_user(user)
    return render_template('games.html', games=games, user=user, is_user_joined=True)


@game_view.route("/active", methods=['GET'])
@login_required
def show_active_games(user):
    games = models.facade.get_active_games_by_user(user)
    return render_template('games.html', games=games, user=user, is_user_joined=True)


@game_view.route('/remove', methods=['GET'])
@login_required
def delete_treasures_function(user):
    game_id = request.args.get('game_id')
    models.facade.delete_game(game_id, user)
    return redirect(url_for("game_views.show_created_games"))


@game_view.route('/join', methods=['GET'])
@login_required
def join_game(user):
    game_id = request.args.get('game_id')
    models.facade.join_game(game_id, user)
    return redirect(url_for("game_views.show_active_games"))


@game_view.route('/unjoin', methods=['GET'])
@login_required
def unjoin_game(user):
    game_id = request.args.get('game_id')
    models.facade.unjoin_game(game_id, user)
    return redirect(url_for("game_views.show_active_games"))
