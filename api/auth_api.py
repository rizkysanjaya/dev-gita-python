from flask import Flask, request, jsonify, make_response, Blueprint, session, redirect, url_for, render_template
from datetime import datetime, timedelta
from db_queries import *
# from app import app


auth_api = Blueprint('auth_api', __name__)


# User list
@auth_api.route('/api/users', methods=['GET'])
@token_required
def getAllUser():
    # check role admin
    # if not admin:

    # :
    data = common_db.selectAllData('users')
    
    if data != 200:
        return data  # Wrap the result in a JSON-friendly dictionary
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500
    
# Configure logging
import logging
logging.basicConfig(level=logging.DEBUG)
    
# Login page
@auth_api.route('/api/login', methods=['POST'])
def login():
    # creates dictionary of form data
    # Parse JSON data from the request body
    jsonObject = request.json
    nip = jsonObject.get('nip')
    password = jsonObject.get('password')
    platform = jsonObject.get('platform')
    time_zone = jsonObject.get('time_zone')

    if not nip or not password:
        return jsonify('NIP and password are required', 400)

    user = checkUser(nip, password)
    # print(user)

    if user:
        token = jwt.encode({'nip': nip,
                            'exp': str(datetime.utcnow() + timedelta(minutes=30))},
                            current_app.config['SECRET_KEY'],
                            algorithm="HS256")
        return jsonify({'token': token,
                        'status': 200,
                        'WWW-Authenticate': 'User Authenticated!'})
    else:
        return jsonify({'message': 'Authentication failed!"',
                        'status' : 401,
                        'WWW-Authenticate': 'Login required!'})

