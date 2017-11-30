from api import app
from flask import Blueprint, request
from .. import db
from api.models import PointsOfInterest, AdditionalLinks, Content,Maps
import json
from flask import jsonify
from api.utils import serializeList
from sqlalchemy import func
import time
from datetime import date
import uuid
from flask_login import LoginManager, login_required, login_user, logout_user 

mod = Blueprint('maps', __name__)

#Gets all maps
@app.route('/maps', methods=['GET'])
def getallyears():
    if request.method == 'GET':
        try:
            return jsonify({'status': 'success', 'data': serializeList((Maps.query.all()))})
        except Exception as ex:
            return jsonify({"status: ": "failed", "message:": str(ex)})
    else:
        return jsonify({"status: ": "failed", "message: ": "Endpoint, /years, needs a GET request"})

#Maps for certain year
@app.route('/maps/<year>', methods=['GET'])
def getmapsforyear(year):
    if request.method == 'GET':
        try:
            return jsonify({'status': 'success', 'data': serializeList((Maps.query.filter(Maps.year==year)))})
        except Exception as ex:
            return jsonify({"status: ": "failed", "message:": str(ex)})
    else:
        return jsonify({"status: ": "failed", "message: ": "Endpoint, /maps, needs a GET or POST request"})

#Add a map
@app.route('/maps', methods=['POST'])
def addmapforyear():
    if request.method == 'POST':
        try:
            json_dict = json.loads(request.data)
            result = Maps(
                image_url = json_dict['image_url'],
                year = (int)(json_dict['year'])
            )
            if Maps.query.filter(Maps.year == json_dict['year']).count():
                Maps.query.filter(Maps.year == json_dict['year']).delete()
                db.session.commit()
            db.session.add(result)
            db.session.commit()
            return jsonify({"status:": "success", "message": "successfully added maps and year"})
        except Exception as ex:
            return jsonify({"status: ": "failed", "message:": str(ex)})
    else:
        return jsonify({"status: ": "failed", "message: ": "Endpoint, /maps, needs a GET or POST request"})

@app.route('/maps/<year>', methods=['GET'])
def years4(year):
    if request.method == 'GET':
        try:
            return jsonify({'status': 'success', 'data': serializeList((Maps.query.filter(Maps.year==year)))})
            #return jsonify(serializeList((Maps.query.filter(Maps.year==year))))
        except Exception as ex:
            return jsonify({"status: ": "failed", "message:": str(ex)})
    else:
        return jsonify({"status: ": "failed", "message: ": "Endpoint, /maps/<year>, needs a GET request"})


# delete maps by id
@app.route('/maps/<id>', methods=['DELETE'])
def delete_map(id):
    try:
        map_to_delete = Maps.query.get(id)
        if map_to_delete is None:
            return jsonify({'status':'failed','message':"maps doesn't exist"})
        year = map_to_delete.year
        poi_to_delete = PointsOfInterest.query.filter(PointsOfInterest.map_by_year == year)
        for obj in poi_to_delete:
            for s in obj.stories:
                db.session.delete(s)
                db.session.commit()
            db.session.delete(obj)
            db.session.commit()
        db.session.delete(map_to_delete)
        db.session.commit()
        return jsonify({"status":'success','message':'successfully deleted'})
    except Exception as ex:
        return jsonify({"status: ": "failed", "message:": str(ex)})
