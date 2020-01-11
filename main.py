from flask import Flask, render_template, redirect, request, session
from google.appengine.ext import db
import os
from views.google_views import google_bp, login_required, get_user
import requests_toolbelt.adapters.appengine
from models.entities.user import User
from models.entities.conversation import Conversation
from models.entities.messages import Message
import time
from views.google_views import google_view
from views.treasure import treasure_view
from views.game import game_view
#from views.twitter_views import twitter_view, twitter_bp
#from views.facebook_views import facebook_view, facebook_bp
from views.profile import profile_view
from views.google import google_view
from views.users import users_routes
from views.zone import zone_routes

import time


# Patch to fix AppEngine
requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(google_bp, url_prefix="/")
#app.register_blueprint(twitter_bp, url_prefix="/")
#app.register_blueprint(facebook_bp, url_prefix="/")
app.register_blueprint(google_view, url_prefix="/google")
#app.register_blueprint(twitter_view, url_prefix="/twitter")
#app.register_blueprint(facebook_view, url_prefix="/facebook")
app.register_blueprint(profile_view, url_prefix="/profile")
app.register_blueprint(treasure_view, url_prefix="/games/treasures")
app.register_blueprint(game_view, url_prefix="/games")


@app.route('/')
@get_user
def home(user=None):
    return render_template('home.html', user=user)


@app.route("/treasure")  # creates a new treasure
def treasures():
    return render_template("treasures.html")


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
id_user = 6578378068983808


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
        cont = 0
        global conversation_global
        conversation_global = []

        search = [0, 1]
        for i in search:
            result = Conversation.all()
            if i == 0:
                r = result.filter("user2 =", id_user)
            else:
                r = result.filter("user1 =", id_user)
            for us in r:
                if i == 0:
                    user_id = us.user1
                else:
                    user_id = us.user2
                user = db.get(db.Key.from_path('User', user_id))
                if cont % 2 == 0:
                    conversation_global.append(
                        {'id': us.key().id(), 'user': user,
                         'color': False}, )
                else:
                    conversation_global.append(
                        {'id': us.key().id(), 'user': user,
                         'color': True}, )
                cont += 1

        return render_template('conversation.html', conversations=conversation_global)


@app.route('/add_conversation/<id>', methods=['GET', 'POST'])
def add_conversation(id):
    global id_user
    user_id = int(id)
    encon = False
    conversation_found = []

    result = Conversation.all()
    filter_conversation = result.filter("user1 = ", user_id)
    for conver in filter_conversation:
        if conver.user2 == id_user:
            encon = True
            conversation_found = conver
            user = conver.user2

    result = Conversation.all()
    filter_conversation = result.filter("user2 = ", user_id)
    for conver in filter_conversation:
        if conver.user1 == id_user:
            encon = True
            conversation_found = conver
            user = conver.user1

    if encon is False:
        user = db.get(db.Key.from_path('User', user_id))
        conversation = Conversation(
            user1=user_id,
            user2=id_user
        )
        conversation.put()

    result = []
    return render_template('message.html', conversations=result, person=user, id=id_user)


@app.route('/listconversation', methods=['GET', 'POST'])
def conversation_list():
    if request.method == 'POST':
        print "post"
    else:
        global id_user
        users = User.all()
        users_to_show = []
        for user in users:
            if user.key().id() != id_user:
                users_to_show.append(user)
        return render_template('list_for_conversation.html', users=users_to_show, id=id_user)


@app.route('/message/<id>', methods=['GET', 'POST'])
def message(id):
    if request.method == 'POST':
        conversation_id = int(id)
        conversation = db.get(db.Key.from_path('Conversation', conversation_id))
        if conversation.user2 == id_user:
            user = db.get(db.Key.from_path('User', conversation.user1))
        else:
            user = db.get(db.Key.from_path('User', conversation.user2))
        all_msg_send = Message.all()
        results = all_msg_send.filter("conversation = ", conversation.key().id())
        message = Message(
            user=id_user,
            message=request.form.get('msg'),
            time=time.asctime(time.localtime(time.time())),
            conversation=conversation_id
        )
        message.put()
        return render_template('message.html', conversations=results, person=user, id=id_user, id_conversation=id)
    else:
        conversation_id = int(id)
        conversation = db.get(db.Key.from_path('Conversation', conversation_id))
        if conversation.user2 == id_user:
            user = db.get(db.Key.from_path('User', conversation.user1))
        else:
            user = db.get(db.Key.from_path('User', conversation.user2))
        all_msg = Message.all()
        result = all_msg.filter("conversation = ", conversation.key().id())
        sortedValue = [value.orden for value in result]
        return render_template('message.html', conversations=sortedValue, person=user, id=id_user, id_conversation=id)


if __name__ == '__main__':
    app.run(debug=True)