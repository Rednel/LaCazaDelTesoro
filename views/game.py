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
    print(len(games))
    return render_template('games.html', games=games, user=user)


@game_view.route('/remove', methods=['GET'])
@login_required
def delete_treasures_function(user):
    game_id = request.args.get('game_id')
    models.facade.delete_game(game_id, user)
    return redirect(url_for("game_views.show_created_games"))
