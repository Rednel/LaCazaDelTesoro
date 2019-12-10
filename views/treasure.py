from flask import render_template, request, Blueprint
import models.facade
from views.google import login_required

treasure_view = Blueprint('treasure_views', __name__)


@treasure_view.route("/", methods=['GET'])
def show_treasures_get():
    treasures = models.facade.get_all_treasures()
    return render_template('treasures.html', treasures=treasures)


@treasure_view.route('/add', methods=['GET'])
def render_treasures_form_get():
    return render_template('new_treasure_form.html')


@treasure_view.route('/add', methods=['POST'])
def render_treasures_form_post():
    lat = request.form.get('inputLatitude')
    lon = request.form.get('inputLongitude')
    des = request.form.get('inputDescription')
    if lat != "" and lon != "":
        models.facade.create_treasure(float(lat), float(lon), des)
        return show_treasures_get()
    else:
        return render_template('new_treasure_form.html')


@treasure_view.route('/remove', methods=['GET'])
def delete_treasures_function():
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    treasure = models.facade.create_treasure(latitude, longitude)
    models.facade.delete_treasure(treasure)
    return show_treasures_get()


@treasure_view.route('/image', methods=['GET'])
def render_treasure_image_view():
    treasure_id = request.args.get('treasure_id')
    treasure = models.facade.get_treasure_by_id(treasure_id)
    print(treasure.images)
    return render_template('treasure_view.html', treasure=treasure)


@treasure_view.route('/image', methods=['POST'])
@login_required
def send_treasure_image(user):
    treasure_id = request.args.get('treasure_id')
    image = request.args.get('image')
    models.facade.update_treasure_image(user=user, treasure_id=treasure_id, img=image)
    return show_treasures_get()


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
