from flask import Flask
from views.treasure import treasure_view

app = Flask(__name__)
app.register_blueprint(treasure_view, url_prefix="/treasures")

if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app
