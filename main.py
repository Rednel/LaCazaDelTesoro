from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


""" 
CRUD User routes       
"""


# user list
@app.route('/user_all')
def user_all():
    return 'Hello World!'


#  get user info
@app.route('/user_one')
def user_one():
    return 'Hello World!'


#  update user info
@app.route('/user_edit')
def user_edit():
    return 'Hello World!'


#  delete user
@app.route('/user_delete')
def user_delete():
    return 'Hello World!'


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
    app.run()
