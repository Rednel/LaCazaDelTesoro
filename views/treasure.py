from flask import render_template, request, Blueprint, redirect, url_for
import models.facade
from views.google import login_required
import json
from views.google_views import login_required

treasure_view = Blueprint('treasure_views', __name__)


@treasure_view.route("/", methods=['GET'])
@login_required
def show_treasures_get(user):
    game_id = request.args.get('game_id')
    game = models.facade.get_game_by_id(game_id=game_id)
    treasures = models.facade.get_all_treasures_by_game(game=game)
    participant_images_tuples = models.facade.get_snapshots_by_game(owner=user, game=game)
    return render_template('treasures.html', game=game, user=user, treasures=treasures,
                           participant_images_tuples=participant_images_tuples)


@treasure_view.route('/add', methods=['GET'])
@login_required
def render_treasures_form_get(user):
    game_id = request.args.get('game_id')
    map_json = request.args.get('map_json')
    game = models.facade.get_game_by_id(game_id=game_id)
    models.facade.write_game_json(game=game, user=user, map_json=map_json)
    game = models.facade.get_game_by_id(game_id=game_id)
    return render_template('new_treasure_form.html', game=game, user=user)


@treasure_view.route('/add', methods=['POST'])
@login_required
def render_treasures_form_post(user):
    name = request.form.get('inputName')
    lat = request.form.get('inputLatitude')
    lon = request.form.get('inputLongitude')
    des = request.form.get('inputDescription')
    if lat != "" and lon != "" and name != "":
        game_id = request.args.get('game_id')
        game = models.facade.get_game_by_id(game_id=game_id)
        models.facade.create_treasure(game=game, user=user, name=name, lat=float(lat), lon=float(lon), description=des)
        return redirect(url_for("treasure_views.show_treasures_get", game_id=game_id))
    else:
        return render_template('new_treasure_form.html')


@treasure_view.route('/remove', methods=['GET'])
@login_required
def delete_treasures_function(user):
    game_id = request.args.get('game_id')
    treasure_id = request.args.get('treasure_id')
    treasure = models.facade.get_treasure_by_id(treasure_id)
    models.facade.delete_treasure(treasure=treasure, user=user)
    return redirect(url_for("treasure_views.show_treasures_get", game_id=game_id))


@treasure_view.route('/image', methods=['GET'])
@login_required
def render_treasure_image_view(user):
    treasure_id = request.args.get('treasure_id')
    game_id = request.args.get('game_id')
    treasure = models.facade.get_treasure_by_id(treasure_id)
    game = models.facade.get_game_by_id(game_id)
    image_base64 = models.facade.get_snapshot_by_user_treasure_in_base_64(user=user, treasure=treasure)
    return render_template('treasure_image.html', treasure=treasure, game=game, image_base64=image_base64, user=user)


@treasure_view.route('/image', methods=['POST'])
@login_required
def send_treasure_image(user):
    treasure_id = request.args.get('treasure_id')
    game_id = request.args.get('game_id')
    image_path = request.files.get('image')
    if image_path != "":
        file_data = image_path.read()
        treasure = models.facade.get_treasure_by_id(treasure_id)
        models.facade.create_snapshot(user=user, treasure=treasure, img=file_data)
        return redirect(url_for("treasure_views.show_treasures_get", game_id=game_id))
    else:
        return redirect(url_for("treasure_views.render_treasure_image_view", game_id=game_id, treasure_id=treasure_id))


@treasure_view.route('/image/delete', methods=['GET'])
@login_required
def delete_treasure_image(user):
    treasure_id = request.args.get('treasure_id')
    game_id = request.args.get('game_id')
    treasure = models.facade.get_treasure_by_id(treasure_id)
    models.facade.delete_snapshot(user=user, treasure=treasure)
    return redirect(url_for("treasure_views.render_treasure_image_view", game_id=game_id, treasure_id=treasure_id))


@treasure_view.route('/image/admin_delete', methods=['GET'])
@login_required
def delete_treasure_image_by_game_admin(user):
    treasure_id = request.args.get('treasure_id')
    game_id = request.args.get('game_id')
    player_id = request.args.get('player_id')
    treasure = models.facade.get_treasure_by_id(treasure_id=treasure_id)
    player = models.facade.get_user_by_user_id(user_id=player_id)
    models.facade.delete_snapshot(user=player, treasure=treasure)
    return redirect(url_for("game_views.view_participant_snapshots", game_id=game_id, player_id=player_id))


