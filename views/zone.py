from flask import Flask, render_template, redirect, request, session, Blueprint
from models.facade import *

zone_routes = Blueprint('zone', __name__)


""" 
Routes Zona        
"""

# zone list
@zone_routes.route('/zone_all')
def zone_all():
    data = get_zone_all()
    return render_template('zone/zone_all.html', data=data)


#  get zone info
@zone_routes.route('/zone_one/<id>')
def zone_one(id):
    zone_id = int(id)
    zone = zone_one_model(zone_id)
    return render_template('zone/zone_one.html', zone=zone)


#  new zone
@zone_routes.route('/zone_new', methods=['GET', 'POST'])
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
@zone_routes.route('/zone_edit/<id>', methods=['GET', 'POST'])
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
@zone_routes.route('/zone_delete/<id>')
def zone_delete(id):
    if id:
        zone_id = int(id)
        zone_delete_model(zone_id)
        return redirect('/zone_all')
