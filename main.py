from flask import Flask, render_template, redirect, request
from google.appengine.ext import db
import os
from views.google_views import google_bp, login_required, google_view, get_user
import requests_toolbelt.adapters.appengine
from models.entities.user import User
from models.entities.game import Game

from models.entities.conversation import Conversation
from models.entities.messages import Message


from views.twitter_views import twitter_view, twitter_bp
from views.facebook_views import facebook_view, facebook_bp
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
app.register_blueprint(twitter_bp, url_prefix="/")
app.register_blueprint(facebook_bp, url_prefix="/")
app.register_blueprint(google_view, url_prefix="/google")
app.register_blueprint(users_routes)
app.register_blueprint(zone_routes)

app.register_blueprint(twitter_view, url_prefix="/twitter")
app.register_blueprint(facebook_view, url_prefix="/facebook")
app.register_blueprint(profile_view, url_prefix="/profile")


@app.route('/')
@get_user
def home(user=None):
    return render_template('home.html', user=user)

@app.route("/treasure")  # creates a new treasure
def treasures():
    return render_template("treasures.html")


@app.route('/test', methods=['GET'])
@login_required
def test_oauth(user):
    return "You are {email} on Google".format(email=user.email)

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
        return render_template('search/game_search.html', data=result)

""" 
CRUD Mensajes       
"""

conversation_global = []
id_user = 6578378068983808


#  new conversation
@app.route('/conversation', methods=['GET', 'POST'])
def conversation_new():
    if request.method == 'POST':
        print "Post"
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
