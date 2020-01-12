from flask import Flask, render_template, request
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
app.register_blueprint(game_view, url_prefix="/games")
app.register_blueprint(treasure_view, url_prefix="/games/treasures")


@app.route('/')
@get_user
def home(user=None):
    return render_template('home.html', user=user)


""" 
CRUD Mensajes       
"""


@app.route('/conversation/all', methods=['GET'])
@login_required
def conversation_list(user_logged):
    users = User.all()
    users_to_show = []
    for user in users:
        if user.key() != user_logged.key():
            users_to_show.append(user)
    return render_template('list_for_conversation.html', user=user_logged, users=users_to_show)


def is_participant_in_chat(element, user):
    return element.user1.key() == user.key() or element.user2.key() == user.key()


@app.route('/conversation/open', methods=['GET'])
@login_required
def add_conversation(user):
    receiver_id = request.args.get('receiver_id')
    receiver_user = models.facade.get_user_by_user_id(receiver_id)
    conversation = Conversation(
        user1=user,
        user2=receiver_user
    )
    user_receiver_conversation = filter(lambda x: is_participant_in_chat(element=x, user=user), Conversation.all())
    if user_receiver_conversation:
        conversation = user_receiver_conversation[0]

    else:
        conversation.put()

    messages = sorted(conversation.messages, key=lambda x: x.time)

    return render_template('message.html', messages=messages, conversation=conversation, user=user,
                           receiver_user=receiver_user)


@app.route('/message', methods=['POST'])
@login_required
def add_message(user):
    conversation_id = request.args.get('conversation_id')
    conversation = Conversation.get(conversation_id)

    message = request.form.get('msg')

    if message != "" and message is not None:
        msg = Message(
            user=user,
            message=message,
            conversation=conversation
        )
        msg.put()

    messages = sorted(conversation.messages, key=lambda x: x.time)
    return render_template('message.html', messages=messages, conversation=conversation, user=user,
                           receiver_user=conversation.user2)


if __name__ == '__main__':
    app.run(debug=True)
