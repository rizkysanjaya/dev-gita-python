from flask import Flask
# from flask import Bearer
from api import *
# from api.book_api import book_api  # Import other blueprints as needed

app = Flask(__name__)

# Configure the app if needed (e.g., database settings)
app.config['SECRET_KEY'] = 'your_secret_key'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'your_database_uri'

# Initialize extensions if used (e.g., SQLAlchemy)
# db = SQLAlchemy(app)

# Register the blueprints
app.register_blueprint(kegiatan_api)
app.register_blueprint(user_api)


# app.register_blueprint(book_api)
# Register other blueprints as needed

# Home
@app.route('/')
def home():
    return 'Welcome to the home page!'

if __name__ == '__main__':
     app.run(debug=True)

# from flask import Flask, render_template, request, redirect, url_for
# from config import db_params
# from flask import jsonify
# import psycopg2
# import psycopg2.extras
# from api.kegiatan_api import kegiatan_api

# app = Flask(__name__)

# # GET ALL USERS DATA
# @app.route("/api/users")
# def users():
#     try:
#         conn = psycopg2.connect(**db_params)
#         cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute("SELECT * FROM users")
#         rows = cursor.fetchall()
#         return jsonify({"data": rows})  # Wrap the result in a JSON-friendly dictionary
#     except (Exception, psycopg2.DatabaseError) as error:
#         # Create a custom error message
#         error_message = {"error": str(error)}  # Convert the error to a string
#         return jsonify(error_message), 500  # Return the error message as JSON with a 500 status code

# # GET USER DATA BY ID
# @app.route("/api/users/<int:id>")
# def user(id):
#     try:
#         conn = psycopg2.connect(**db_params)
#         cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#         cursor.execute("SELECT * FROM users WHERE id = %s", (id,))
#         row = cursor.fetchone()

#         if row is None:
#             # If no data found, return a "no record available" message
#             return jsonify({"message": "Data user tidak ditemukan"}), 404  # 404 indicates "Not Found"
#         else:
#             # If data found, return the user data
#             return jsonify({"data": row})  # Wrap the result in a JSON-friendly dictionary

#     except (Exception, psycopg2.DatabaseError) as error:
#         # Create a custom error message
#         error_message = {"error": str(error)}
#         return jsonify(error_message), 500  # Return the error message as JSON with a 500 status code

#     # conn = psycopg2.connect(**db_params)
#     # cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     # cursor.execute("SELECT * FROM users")
#     # bookRows = cursor.fetchall()
#     # return render_template('books.html', title='Books', books=bookRows)

# if __name__ == "__main__":
#     app.run(debug=True)