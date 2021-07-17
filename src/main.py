"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Favorite
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def handle_hello():
    all_users = User.query.all()
    all_users = list(map(lambda user: user.serialize(),all_users))
    response_body = {
        "user": all_users
    }

    return jsonify(response_body), 200

@app.route('/<user>/favorites', methods=['GET'])
def get_favorites(user):
    single_user = User.query.filter_by(username=user).first()
    if single_user is None:
        raise APIException("User not found", status_code=404)
    favorites = Favorite.query.filter_by(username=user)
    all_favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    response_body = {
        "favorites": all_favorites
    }

    return jsonify(response_body), 200

@app.route('/favorite/planet/<int:id>', methods=['POST','DELETE'])
def add_planet(id):
    request_body = request.get_json()
    if request_body is None or request_body == {}:
        raise APIException("Empty body", status_code=404)
    if request.method == 'POST':
        planet = Favorite(name=request_body["name"], entity_type="planet", entity_id=id, username=request_body["username"])
        db.session.add(planet)
        db.session.commit()
    else:
        deleted_planet = Favorite.query.filter_by(entity_type='planet', entity_id=id, username=request_body["username"]).first()
        if deleted_planet is None:
            raise APIException("planet not found", status_code=404)
        db.session.delete(deleted_planet)
        db.session.commit()
    favorites = Favorite.query.filter_by(username=request_body["username"])
    all_favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    response_body = {
        "favorites": all_favorites
    }

    return jsonify(response_body), 200

@app.route('/favorite/person/<int:id>', methods=['POST','DELETE'])
def add_person(id):
    request_body = request.get_json()
    if request_body is None or request_body == {}:
        raise APIException("Empty body", status_code=404)
    if request.method == 'POST':
        record = Favorite.query.filter_by(username=request_body["username"], name=request_body["name"]).first()
        if record:
            raise APIException("Favorite already exists", status_code=418)
        person = Favorite(name=request_body["name"], entity_type="person", entity_id=id, username=request_body["username"])
        db.session.add(person)
        db.session.commit()
    else:
        deleted_person = Favorite.query.filter_by(entity_type='person', entity_id=id, username=request_body["username"]).first()
        if deleted_person is None:
            raise APIException("person not found", status_code=404)
        db.session.delete(deleted_person)
        db.session.commit()
    favorites = Favorite.query.filter_by(username=request_body["username"])
    all_favorites = list(map(lambda favorite: favorite.serialize(), favorites))
    response_body = {
        "favorites": all_favorites
    }

    return jsonify(response_body), 200


# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
