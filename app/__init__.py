# app/__init__.py
import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy

from flask import request, jsonify, abort, make_response

# local import

from instance.config import app_config

# initialize db
db = SQLAlchemy()


def create_app(config_name):

    from app.models import Resourcelist

    app = FlaskAPI(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/resourcedetails/', methods=['POST'])
    def resourcelists():    
        skill = str(request.data.get('skillset', ''))
        bucketlists = Resourcelist.get_all(skill)
        results = []

        for bucketlist in bucketlists:
            obj = {
                'id': bucketlist.id,
                'name': bucketlist.name
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response
    return app