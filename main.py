from flask import Flask, render_template, redirect, request, session
from google.appengine.ext import db
import os
from views.google import google_bp, login_required
import requests_toolbelt.adapters.appengine
from models.entities.user import User
from models.entities.conversation import Conversation
from models.entities.messages import Message

import time
from views.google import google_view
from models.facade import *

# Patch to fix AppEngine
requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(google_bp, url_prefix="/")
app.register_blueprint(google_view, url_prefix="/google")


@app.route('/')
def home():

    return render_template('index.html')


@app.route("/treasure")  # creates a new treasure
def treasures():
    return render_template("treasures.html")


@app.route('/test', methods=['GET'])
@login_required
def test_oauth(user):
    return "You are {email} on Google".format(email=user.email)


""" 
User routes       
"""


# user list
@app.route('/user_all')
def user_all():
    data = get_all_user()
    return render_template('user/user_all.html', data=data)


#  get user info
@app.route('/user_one/<id>')
def user_one(id):
    user_id = int(id)
    user = get_user_one(user_id)
    return render_template('user/user_one.html', user=user)


#  new user
@app.route('/user_new', methods=['GET', 'POST'])
def user_new():
    if request.method == 'POST':
        email = request.form.get('email'),
        name = request.form.get('name'),
        surname = request.form.get('surname'),
        picture = request.form.get('picture')
        insert_user_new(email, name, surname, picture)
        return redirect('user_all')
    else:
        return render_template('user/user_new.html')



#  update user info
@app.route('/user_edit/<id>', methods=['GET', 'POST'])
def user_edit(id):
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        surname = request.form.get('surname')
        picture = request.form.get('pricture')
        user_id = int(id)
        user_update_model(id, name, email, surname, picture)
        return redirect('/user_all')
    else:
        user_id = int(id)
        user = db.get(db.Key.from_path('User', user_id))
        return render_template('user/user_edit.html', user=user)


#  delete user
@app.route('/user_delete/<id>')
def user_delete(id):
    if id:
        user_id = int(id)
        user_delete_model(user_id)
        return redirect('/user_all')

""" 
Routes Zona        
"""


# zone list
@app.route('/zone_all')
def zone_all():
    data = get_zone_all()
    return render_template('zone/zone_all.html', data=data)


#  get zone info
@app.route('/zone_one/<id>')
def zone_one(id):
    zone_id = int(id)
    zone = zone_one_model(zone_id)
    return render_template('zone/zone_one.html', zone=zone)


#  new zone
@app.route('/zone_new', methods=['GET', 'POST'])
def zone_new():
    if request.method == 'POST':
        name = request.form.get('name')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        height = request.form.get('height')
        width = request.form.get('width')
        insert_zone_new(name, latitude, longitude, height, width)
        return redirect('zone_all')
    else:
        return render_template('zone/zone_new.html')
    zone_new()


#  update zone info
@app.route('/zone_edit/<id>', methods=['GET', 'POST'])
def zone_edit(id):
        if request.method == 'POST':
            name = request.form.get('name')
            latitude = request.form.get('latitude')
            longitude = request.form.get('longitude')
            height = request.form.get('height')
            width = request.form.get('width')
            zone_id = int(id)
            zone_edit_model(id, name, latitude, longitude, height, width)
            return redirect('/zone_all')
        else:
            zone_id = int(id)
            zone = db.get(db.Key.from_path('Zone', zone_id))
            return render_template('zone/zone_edit.html', zone=zone)


#  delete zone
@app.route('/zone_delete/<id>')
def zone_delete(id):
    if id:
        zone_id = int(id)
        zone_delete_model(zone_id)
        return redirect('/zone_all')

""" 
SEARCH FOR GAME       
"""
@app.route('/game_search',methods=['POST'])
def game_search():
    keyword = request.form.get('keyword')
    if keyword:
        keyword = str(keyword)
        q = Game.all()
        result = q.filter("game_name =", keyword)
        return render_template('game_search.html', data=result)


""" 
CRUD Mensajes       
"""

conversation_global = []
id_user = 3


#  new conversation
@app.route('/conversation', methods=['GET', 'POST'])
def conversation_new():
    if request.method == 'POST':
        conversation = Conversation(
            user=User()
        )
        conversation.put()
        return redirect('')
    else:
        global conversation_global
        conversation_global = []
        conversation_global.append({'id': 1, 'user': 'Ayad', 'color': False}, )
        conversation_global.append({'id': 2, 'user': 'Tarek', 'color': True}, )
        conversation_global.append({'id': 1, 'user': 'Alberto', 'color': False}, )
        conversation_global.append({'id': 2, 'user': 'Sergio', 'color': True}, )
        return render_template('conversation.html', conversations=conversation_global)


@app.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':
        message = Message(
            user=User(),
            message=request.form.get('msg'),
            time=time.asctime(time.localtime(time.time())),
            conversation=Conversation()
        )
        message.put()
        return redirect('')
    else:
        result = []
        # pasar el usuario para empezar a enviar mensajes
        result_send = get_person(1)
        return render_template('message.html', conversations=result, person=result_send, id=id_user)


def get_person(id):
    for i in conversation_global:
        if i['id'] is int(id):
            return i['user']


def get_conversations_of_the_user_id(id):
    conversations = db.conversation

    global conversation_global

    user_conversation = conversations.find({
        'members.iduser': int(id)
    })
    cont = 0
    for i in user_conversation:
        if i['members'][0]['iduser'] == int(id):
            if cont % 2 == 0:
                conversation_global.append({'id': i['id'], 'user': i['members'][1], 'color': False}, )
            else:
                conversation_global.append({'id': i['id'], 'user': i['members'][1], 'color': True}, )
        else:
            if cont % 2 == 0:
                conversation_global.append({'id': i['id'], 'user': i['members'][0], 'color': False}, )
            else:
                conversation_global.append({'id': i['id'], 'user': i['members'][0], 'color': True}, )
        cont += 1
    return conversation_global


if __name__ == '__main__':
    app.run(debug=True)
