from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/treasure")  # creates a new treasure
def treasures():
    return render_template("treasures.html")


if __name__ == "__main__":  # on running python app.py
    app.run(debug=True)  # run the flask app



