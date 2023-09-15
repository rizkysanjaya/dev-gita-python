from flask import Blueprint, Flask, render_template, request, redirect, url_for
from config import db_params
from flask import jsonify
import psycopg2
import psycopg2.extras

user_api = Blueprint('user_api', __name__)

@user_api.route('/api/users')
def getAllUser():
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        if rows is None:
            # If no data found, return a "no record available" message
            return jsonify({"message": "Belum ada data user"}), 404  # 404 indicates "Not Found"
        else:
            # If data found, return the user data
            return jsonify({"data": rows})  # Wrap the result in a JSON-friendly dictionary
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500  # Return the error message as JSON with a 500 status code
