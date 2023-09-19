# from flask import Blueprint, Flask, render_template, request, redirect, url_for, make_response
# from config import db_params
# from flask import jsonify
# import psycopg2
# import psycopg2.extras
# from db_queries import *

# user_api = Blueprint('user_api', __name__)

# @user_api.route('/api/userALL')
# def getAllUser():
#     # check role admin
#     # if not admin:

#     # :
#     data = common_db.selectAllData('users')
    
#     if data != 200:
#         return data  # Wrap the result in a JSON-friendly dictionary
#     else:
#         return jsonify({"message": "Kesalahan pada server."}), 500
