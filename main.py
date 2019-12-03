from flask import Flask, render_template
import models.facade

app = Flask(__name__)


@app.route('/')
def get_treasures():
    treasures = models.facade.get_treasures()
    return render_template('treasures.html', treasures=treasures)


@app.route('/addTreasure/lat=<latitude>&long=<longitude>&description=<description>')
def add_treasure(latitude, longitude, description):
    models.facade.create_treasure(float(latitude), float(longitude), description)
    treasures = models.facade.get_treasures()
    return render_template('treasures.html', treasures=treasures)


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
