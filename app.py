from flask import Flask, render_template, request, redirect, url_for, jsonify, Blueprint
# from flask import Bearer
from api import *

# auth_api = Blueprint('auth_api', __name__)
# from api.book_api import book_api  # Import other blueprints as needed

app = Flask(__name__, template_folder="templates")

# Configure the app if needed (e.g., database settings)
app.config['SECRET_KEY'] = 'e496637306e54c40875b814ed38a6476'

# Register the blueprints
app.register_blueprint(kegiatan_api)
# app.register_blueprint(user_api)
app.register_blueprint(auth_api)


# app.register_blueprint(book_api)
# Register other blueprints as needed

# Home
@app.route('/')
def home():
    return render_template('home.html')


if __name__ == '__main__':
     app.run(debug=True)

