from flask import render_template, request, Blueprint
import models.facade

treasure_view = Blueprint('treasure_views', __name__)


@treasure_view.route("/", methods=['GET'])
def show_treasures():
    if request.method == 'GET':
        return show_treasures_get()


def show_treasures_get():
    treasures = models.facade.get_treasures()
    return render_template('treasures.html', treasures=treasures)


@treasure_view.route('/add', methods=['GET', 'POST'])
def render_treasures_form():
    if request.method == 'GET':
        return add_treasure_get()
    if request.method == 'POST':
        return add_treasure_post()


def add_treasure_get():
    return render_template('new_treasure_form.html')


def add_treasure_post():
    lat = request.form.get('inputLatitude')
    lon = request.form.get('inputLongitude')
    des = request.form.get('inputDescription')
    if lat != "" and lon != "":
        print(lat)
        print(lon)
        models.facade.create_treasure(float(lat), float(lon), des)
        return show_treasures_get()
    else:
        return render_template('new_treasure_form.html')


@treasure_view.route('/remove/latitude=<latitude>&longitude=<longitude>', methods=['GET'])
def delete_treasures_function(latitude, longitude):
    if request.method == 'GET':
        return remove_treasure_get(float(latitude), float(longitude))


def remove_treasure_get(latitude, longitude):
    treasure = models.facade.create_treasure(latitude, longitude)
    models.facade.remove_treasure(treasure)
    return show_treasures_get()
