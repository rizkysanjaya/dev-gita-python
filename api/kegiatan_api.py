from flask import Blueprint, Flask, render_template, request, redirect, url_for
from flask import jsonify
import psycopg2
import psycopg2.extras
from db_queries import *

kegiatan_api = Blueprint('kegiatan_api', __name__)

# CREATE KEAGIATAN
@kegiatan_api.route('/api/kegiatan', methods=['POST'])
def createKegiatan():
    try:

        jsonObject = request.json

        nama_kegiatan = jsonObject.get('nama_kegiatan')
        tanggal = jsonObject.get('tanggal')
        jam_mulai = jsonObject.get('jam_mulai')
        jam_selesai = jsonObject.get('jam_selesai')
        zona_waktu = jsonObject.get('zona_waktu')
        tempat = jsonObject.get('tempat')
        status = jsonObject.get('status')
        is_draft = jsonObject.get('is_draft')
        # Create a list of values to pass to 'addKegiatan'
        values = [nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft]

        # Call the 'addKegiatan' function with the extracted 'values'
        result, status_code = addKegiatan(values)

        # Return a response indicating success or failure
        return result, status_code
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500

    
# UPDATE KEGIATAN by ID
@kegiatan_api.route('/api/kegiatan/<int:id>', methods=['PUT'])
def updateKegiatan(id):
    try:
        jsonObject = request.json

        nama_kegiatan = jsonObject.get('nama_kegiatan')
        tanggal = jsonObject.get('tanggal')
        jam_mulai = jsonObject.get('jam_mulai')
        jam_selesai = jsonObject.get('jam_selesai')
        zona_waktu = jsonObject.get('zona_waktu')
        tempat = jsonObject.get('tempat')
        status = jsonObject.get('status')
        is_draft = jsonObject.get('is_draft')

        values = [nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft]
        data = kegiatan_db.editKegiatan(values, (id))
        if data != 200:
            return data
        else:
            return jsonify({"message": "Kesalahan pada server."}), 500
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500



# GET ALL KEGIATAN
@kegiatan_api.route('/api/kegiatan', methods=['GET'])
def getKegiatan():
    data = common_db.selectAllData('kegiatan')
    
    if data != 200:
        return data  # Wrap the result in a JSON-friendly dictionary
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# GET KEGIATAN DRAFT    
@kegiatan_api.route('/api/kegiatan/draft', methods=['GET'])
def getDraftKegiatan():
    data = common_db.selectAllData('kegiatan', 'is_draft = 1')
    
    if data != 200:
        return data  # Wrap the result in a JSON-friendly dictionary
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# GET KEGIATAN by ID
@kegiatan_api.route('/api/kegiatan/<int:id>', methods=['GET'])
def getDetailKegiatan(id):
    data = common_db.selectAllData('kegiatan', f'id = {id}')

    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500
    

# CANCEL KEGIATAN (SET STATUS TO BATAL)
@kegiatan_api.route('/api/kegiatan/batal', methods=['POST'])
def batalKegiatan():
    
    _id = request.json['id_kegiatan']
    data = kegiatan_db.cancelKegiatan(_id)
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500

# DELETE KEGIATAN by ID
@kegiatan_api.route('/api/kegiatan/<int:id>', methods=['DELETE'])
def hapusKegiatan(id):
    data = common_db.deleteData('kegiatan', (id))
    if data != 200:
        return data
    else:
        return jsonify({"message": "Kesalahan pada server."}), 500