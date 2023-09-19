from flask import jsonify, request
from config import db_params
import psycopg2
import psycopg2.extras
from  werkzeug.security import generate_password_hash, check_password_hash
# imports for PyJWT authentication
from datetime import datetime, timedelta
import jwt
from functools import wraps
from flask import current_app
# import models
import logging
logging.basicConfig(level=logging.DEBUG)
# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# decorator for verifying the JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            # current_user = checkUser(data['nip'])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid bro'}), 401
        except Exception as e:
            print("Token Decoding Error:", str(e))  # Add this line for debugging
            return jsonify({'message': 'Token decoding error'}), 401

        # return f(current_user, *args, **kwargs)

    return decorated

# Check user in db
def checkUser(nip, password):
    try:
        query = f"SELECT * FROM users WHERE nip = '{nip}' AND password = '{password}'"
        cur.execute(query)
        user = cur.fetchone()
        if user is None:
            return jsonify({'message' : 'User not found!'}), 404
        else:
            cur.execute(f"SELECT nip FROM users WHERE nip = '{nip}' AND password = '{password}'")
            user_nip = cur.fetchone()
            return user_nip  # User found
 
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500

# generate token
# def generateToken(nip):
#     try:
#         # set up a payload with an expiration time
#         payload = {
#             'exp': datetime.utcnow() + timedelta(minutes=30),
#             'iat': datetime.utcnow(),
#             'sub': nip
#         }
#         # create the byte string token using the payload and the SECRET key
#         jwt_string = jwt.encode(
#             payload,
#             app.config['SECRET_KEY'],
#             algorithm='HS256'
#         )
#         return jwt_string.decode('UTF-8')
#     except Exception as e:
#         # return an error in string format if an exception occurs
#         error_message = {"Oops, there's an error.. ": str(e)}
#         return jsonify(error_message), 500
    
# def generate_jwt(payload, lifetime=None):
#     # Generates a new JWT token, wrapping information provided by payload (dict)
#     # Lifetime describes (in minutes) how much time the token will be valid
#     if lifetime:
#         payload['exp'] = (datetime.now() + timedelta(minutes=lifetime)).timestamp()
#     return jwt.encode(payload, app.config['SECRET_KEY'], algorithm="HS256")

# def decode_jwt(token):
#     # Tries to retrieve payload information inside of a existent JWT token (string)
#     # Will throw an error if the token is invalid (expired or inconsistent)
#     return jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])

# def check_jwt():
#     # Gets token from request header and tries to get it's payload
#     # Will raise errors if token is missing, invalid or expired 
#     token = request.headers.get('Authorization')
#     if not token:
#         raise Exception('Missing access token')
#     jwt = token.split('Bearer ')[1]
#     try:
#         return decode_jwt(jwt)
#     except Exception as e:
#         raise Exception(f'Invalid access token: {e}')
    
# def auth_guard(role=None):
#     def wrapper(route_function):
#         def decorated_function(*args, **kwargs):
#             # Authentication gate
#             try:
#                 user_data = check_jwt()
#             except Exception as e:
#                 return jsonify({"message": f'{e}', "status": 401}), 401
#             # Authorization gate
#             if role and role not in user_data['role']:
#                 return jsonify({"message": 'Authorization required.', "status": 403}), 403
#             # Proceed to original route function
#             return route_function(*args, **kwargs)
#         decorated_function.__name__ = route_function.__name__
#         return decorated_function
#     return wrapper