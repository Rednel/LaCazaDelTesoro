from flask import Flask, render_template, redirect, request, session, Blueprint, jsonify
from models.facade import *

users_routes = Blueprint('user', __name__)


""" 
User routes       
"""


# user list
@users_routes.route('/user_all')
def user_all():
    data = get_all_user()
    return render_template('user/user_all.html', data=data)


#  get user info
@users_routes.route('/user_one/<id>')
def user_one(id):
    user_id = int(id)
    user = get_user_by_user_id(user_id)
    return render_template('user/user_one.html', user=user)


#  new user
@users_routes.route('/user_new', methods=['GET', 'POST'])
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
@users_routes.route('/user_edit/<id>', methods=['GET', 'POST'])
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
@users_routes.route('/user_delete/<id>')
def user_delete(id):
    if id:
        user_id = int(id)
        user_delete_model(user_id)
        return redirect('/user_all')

