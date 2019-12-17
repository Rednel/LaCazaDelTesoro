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
