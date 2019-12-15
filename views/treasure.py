from flask import render_template, request, Blueprint, redirect, url_for
import models.facade
from views.google import login_required

treasure_view = Blueprint('treasure_views', __name__)


@treasure_view.route("/", methods=['GET'])
@login_required
def show_treasures_get(user):
    game_id = request.args.get('game_id')
    game = models.facade.get_game_by_id(game_id=game_id)
    treasures = models.facade.get_all_treasures_by_game(game=game)
    participant_images_tuples = list()
    for participant in game.participants:
        number_of_images = len(filter(lambda image: image.treasure in game.treasures, participant.user.images))
        participant_images_tuples.append((participant.user, number_of_images))

    return render_template('treasures.html', game=game, user=user, treasures=treasures,
                           participant_images_tuples=participant_images_tuples)


@treasure_view.route('/add', methods=['GET'])
def render_treasures_form_get():
    game_id = request.args.get('game_id')
    game = models.facade.get_game_by_id(game_id=game_id)
    return render_template('new_treasure_form.html', game=game)


@treasure_view.route('/add', methods=['POST'])
@login_required
def render_treasures_form_post(user):
    lat = request.form.get('inputLatitude')
    lon = request.form.get('inputLongitude')
    des = request.form.get('inputDescription')
    if lat != "" and lon != "":
        game_id = request.args.get('game_id')
        game = models.facade.get_game_by_id(game_id=game_id)
        models.facade.create_treasure(game, user, float(lat), float(lon), des)
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
    return render_template('treasure_image.html', treasure=treasure, game=game, image_base64=image_base64)


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


"""
TODO
    Hacer vista imagen tesoro
    La vista contendra la imagen del tesoro si la tuviera y una opcion para subir una imagen de tesoro
    
    if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

"""
