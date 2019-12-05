from flask import Flask, render_template, redirect, request, session
from google.appengine.ext import db
import os
from views.google import google_bp, login_required
import requests_toolbelt.adapters.appengine
from models.entities.user import User
from views.google import google_view

# Patch to fix AppEngine
requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(google_bp, url_prefix="/")
app.register_blueprint(google_view, url_prefix="/google")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/test', methods=['GET'])
@login_required
def test_oauth(user):
    return "You are {email} on Google".format(email=user.email)


""" 
CRUD User routes       
"""


# user list
@app.route('/user_all')
def user_all():
    data = User.all()
    return render_template('user_all.html', data=data)


#  get user info
@app.route('/user_one/<id>')
def user_one(id):
    user_id = int(id)
    user = db.get(db.Key.from_path('User', user_id))
    return render_template('user_one.html', user=user)


#  new user
@app.route('/user_new', methods=['GET', 'POST'])
def user_new():
    if request.method == 'POST':
        user = User(
            user_name=request.form.get('username'),
            email=request.form.get('email'),
            first_name=request.form.get('firstname'),
            last_name=request.form.get('lastname'),
            gender=request.form.get('gender'),
            role='user'  # por defecto
        )
        user.put()
        return redirect('/user_all')
    else:
        return render_template('user_new.html')


#  update user info
@app.route('/user_edit/<id>', methods=['GET', 'POST'])
def user_edit(id):
    if request.method == 'POST':
        user_id = int(id)
        user = db.get(db.Key.from_path('User', user_id))
        user.user_name = str(request.form.get('username'))
        user.email = str(request.form.get('email'))
        user.first_name = 'Tarek'
        user.last_name = 'Khalfaoui'
        user.gender = 'male'
        user.role = 'user'
        user.put()
        return redirect('/user_all')

    else:
        user_id = int(id)
        user = db.get(db.Key.from_path('User', user_id))
        return render_template('user_edit.html', user=user)


#  delete user
@app.route('/user_delete/<id>')
def user_delete(id):
    user_id = int(id)
    user = db.get(db.Key.from_path('User', user_id))
    db.delete(user)
    return redirect('/user_all')


""" 
CRUD Zona routes       
"""


# zona list
@app.route('/zona_all')
def zona_all():
    return 'Hello World!'


#  get zona info
@app.route('/zona_one')
def zona_one():
    return 'Hello World!'


#  update zona info
@app.route('/zona_edit')
def zona_edit():
    return 'Hello World!'


#  delete zona
@app.route('/zona_delete')
def zona_delete():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
