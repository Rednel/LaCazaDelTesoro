from flask import Flask, render_template, redirect, request, session
from google.appengine.ext import db
import os
from views.google_views import google_bp, login_required, get_user, google_view
import requests_toolbelt.adapters.appengine
from models.entities.user import User
from models.entities.conversation import Conversation
from models.entities.messages import Message
from views.treasure import treasure_view
from views.game import game_view
from views.twitter_views import twitter_view, twitter_bp
from views.facebook_views import facebook_view, facebook_bp
from views.profile import profile_view

import models.facade

import time

# Patch to fix AppEngine
requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

app.register_blueprint(google_bp, url_prefix="/")
app.register_blueprint(twitter_bp, url_prefix="/")
app.register_blueprint(facebook_bp, url_prefix="/")
app.register_blueprint(google_view, url_prefix="/google")
app.register_blueprint(twitter_view, url_prefix="/twitter")
app.register_blueprint(facebook_view, url_prefix="/facebook")
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


#  new conversation
@app.route('/conversation', methods=['GET', 'POST'])
@login_required
def conversation_new(user):
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
                r = result.filter("user2 =", user)
            else:
                r = result.filter("user1 =", user)
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


@app.route('/conversation/add', methods=['GET', 'POST'])
@login_required
def add_conversation(user):
    receiver_id = request.args.get('receiver_id')
    receiver_user = models.facade.get_user_by_user_id(receiver_id)
    chat_found = False
    all_conversations = Conversation.all()
    conversation = Conversation(
        user1=user,
        user2=receiver_user
    )

    filter_conversation = all_conversations.filter("user1 = ", user) and all_conversations.filter("user2 = ", user)
    for chat in filter_conversation:
        if chat.user1 == receiver_user or chat.user2 == receiver_user:
            chat_found = True
            conversation = chat

    if chat_found is False:
        conversation.put()

    return render_template('message.html', conversation=conversation, user=user, receiver_user=receiver_user)


@app.route('/conversation/all', methods=['GET', 'POST'])
@login_required
def conversation_list(user_logged):
    if request.method == 'POST':
        print "post"
    else:
        users = User.all()
        users_to_show = []
        for user in users:
            if user.key() != user_logged.key():
                users_to_show.append(user)
        return render_template('list_for_conversation.html', user=user_logged, users=users_to_show)


@app.route('/message', methods=['GET', 'POST'])
@login_required
def message(user):
    conversation_id = request.args.get('conversation_id')
    conversation = Conversation.get(conversation_id)
    if request.method == 'POST':
        if conversation.user2 == user:
            user = db.get(db.Key.from_path('User', conversation.user1))
        else:
            user = db.get(db.Key.from_path('User', conversation.user2))
        all_msg_send = Message.all()
        results = all_msg_send.filter("conversation = ", conversation.key().id())
        msg = Message(
            user=user,
            message=request.form.get('msg'),
            time=time.asctime(time.localtime(time.time())),
            conversation=conversation_id
        )
        msg.put()
        return render_template('message.html', conversations=results, person=user, id=user, id_conversation=id)
    else:
        if conversation.user2 == user:
            user = db.get(db.Key.from_path('User', conversation.user1))
        else:
            user = db.get(db.Key.from_path('User', conversation.user2))
        all_msg = Message.all()
        result = all_msg.filter("conversation = ", conversation.key().id())
        sorted_value = [value.orden for value in result]
        return render_template('message.html', conversations=sorted_value, person=user, id=user, id_conversation=id)


if __name__ == '__main__':
    app.run(debug=True)
