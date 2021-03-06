from flask import render_template, request, Blueprint, redirect, url_for
import models.facade
from views.google_views import login_required
from views.twitter_views import send_twitter_message_init, send_twitter_message_finished
from views.facebook_views import send_facebook_message_init, send_facebook_message_finished

game_view = Blueprint('game_views', __name__)


@game_view.route("/", methods=['GET'])
@login_required
def show_not_joined_games(user):
    games = models.facade.get_games_not_joined_by_user(user)
    return render_template('games.html', games=games, user=user)


@game_view.route('/add', methods=['GET'])
@login_required
def render_games_form_get(user):
    return render_template('new_game_form.html', user=user)


@game_view.route('/add', methods=['POST'])
@login_required
def render_games_form_post(user):
    name = request.form.get('inputGameName')
    if name != "":

        exists = models.facade.exists_game(game_name=name, user=user)

        if exists:
            return redirect(url_for("game_views.render_games_form_post"))
        else:
            game = models.facade.get_or_insert_game(name=name, owner=user)
            try:
                send_twitter_message_init(game=game)
            except Exception:
                return "Error Twitter"
            try:
                send_facebook_message_init(game=game)
            except Exception:
                return "Error Facebook"

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
    models.facade.unjoin_game(game_id=game_id, user=user)
    return redirect(url_for("game_views.show_active_games"))


@game_view.route('/snapshots', methods=['GET'])
@login_required
def view_participant_snapshots(user):
    game_id = request.args.get('game_id')
    player_id = request.args.get('player_id')
    game = models.facade.get_game_by_id(game_id=game_id)
    player = models.facade.get_user_by_user_id(user_id=player_id)
    user_snapshots = models.facade.get_snapshots_by_game_and_user(game=game, owner=user, user=player)
    return render_template('participant_images_resume.html', game=game, user=user, player=player,
                           user_snapshots=user_snapshots)


@game_view.route('/win', methods=['GET'])
@login_required
def win_game(owner):
    game_id = request.args.get('game_id')
    winner_id = request.args.get('winner_id')
    game = models.facade.get_game_by_id(game_id=game_id)
    winner = models.facade.get_user_by_user_id(user_id=winner_id)
    game = models.facade.win_game(game=game, winner=winner, owner=owner)
    send_twitter_message_finished(game)
    send_facebook_message_finished(game)
    return render_template('winner.html', game=game, user=owner)


@game_view.route('/reopen', methods=['GET'])
@login_required
def reopen_game(user):
    game_id = request.args.get('game_id')
    game = models.facade.get_game_by_id(game_id=game_id)
    models.facade.reopen_game(game=game, user=user)
    return redirect(url_for("game_views.show_created_games"))
