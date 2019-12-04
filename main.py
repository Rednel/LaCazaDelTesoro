from flask import Flask, render_template, request
import models.facade

app = Flask(__name__)


@app.route('/showTreasures', methods=['GET'])
def render_treasures_view():
    if request.method == 'GET':
        return show_treasures_get()


@app.route('/addTreasure', methods=['GET', 'POST'])
def render_treasures_form():
    if request.method == 'GET':
        return add_treasure_get()
    if request.method == 'POST':
        return add_treasure_post()


@app.route('/removeTreasure/latitude=<latitude>&longitude=<longitude>', methods=['GET'])
def delete_treasures_function(latitude, longitude):
    if request.method == 'GET':
        id = str(latitude) + '_' + str(longitude)
        return remove_treasure_post(id)


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app


def show_treasures_get():
    treasures = models.facade.get_treasures()
    return render_template('treasures.html', treasures=treasures)


def add_treasure_get():
    return render_template('new_treasure_form.html')


def add_treasure_post():
    models.facade.create_treasure(float(request.form['inputLatitude']), float(request.form['inputLongitude']),
                                  request.form['inputDescription'])
    return show_treasures_get()


def remove_treasure_post(id_to_remove):
    models.facade.remove_treasure(id_to_remove)
    return show_treasures_get()
