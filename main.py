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
                conversation_global.append({'id': i['id'], 'user': i['members'][1], 'color': False},)
            else:
                conversation_global.append({'id': i['id'], 'user': i['members'][1], 'color': True},)
        else:
            if cont % 2 == 0:
                conversation_global.append({'id': i['id'], 'user': i['members'][0], 'color': False},)
            else:
                conversation_global.append({'id': i['id'], 'user': i['members'][0], 'color': True},)
        cont += 1
    return conversation_global


if __name__ == '__main__':
    app.run(debug=True)
