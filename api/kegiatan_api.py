from flask import Blueprint, Flask, render_template, request, redirect, url_for, make_response
from config import db_params
from flask import jsonify
import psycopg2
import psycopg2.extras
from db_queries import *

kegiatan_api = Blueprint('kegiatan_api', __name__)

@kegiatan_api.route('/api/kegiatan')
def getAllKegiatan():
    try:    
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM kegiatan")
        rows = cursor.fetchall()
        if rows is None:
            # If no data found, return a "no record available" message
            return jsonify({"message": "Belum ada data kegiatan"}), 404  # 404 indicates "Not Found"
        else:
            for row in rows:
                row['jam_mulai'] = row['jam_mulai'].strftime("%H:%M")
                row['jam_selesai'] = row['jam_selesai'].strftime("%H:%M")
            
            # Create a JSON response with a list of records
            response_data = {"data": rows}
            return jsonify(response_data)
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500  # Return the error message as JSON with a 500 status code

# CREATE KEAGIATAN
@kegiatan_api.route('/api/kegiatan', methods=['POST'])
def createKegiatan():
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


# Select kegiatan is_draft

@kegiatan_api.route('/api/kegiatan/draft')
def getDraftKegiatan():
    try:    
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM kegiatan WHERE is_draft = 1")
        rows = cursor.fetchall()
        if rows is None:
            # If no data found, return a "no record available" message
            return jsonify({"message": "Belum ada data kegiatan"}), 404  # 404 indicates "Not Found"
        else:
            for row in rows:
                row['jam_mulai'] = row['jam_mulai'].strftime("%H:%M")
                row['jam_selesai'] = row['jam_selesai'].strftime("%H:%M")
            
            # Create a JSON response with a list of records
            response_data = {"data": rows}
            return jsonify(response_data)
           
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500
    

# Get Keagiatan by id

@kegiatan_api.route('/api/kegiatan/<int:id>')
def getKegiatanById(id):
    try:    
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM kegiatan WHERE id = %s", (id,))
        row = cursor.fetchone()
        if row is None:
            # If no data found, return a "no record available" message
            return jsonify({"message": "Data kegiatan tidak ditemukan"}), 404  # 404 indicates "Not Found"
        else:
            formatted_time1 = row['jam_mulai'].strftime("%H:%M")
            formatted_time2 = row['jam_selesai'].strftime("%H:%M")

            # Include the formatted time columns in the row dictionary
            row['jam_mulai'] = formatted_time1
            row['jam_selesai'] = formatted_time2

            # Create a JSON response with all columns
            response_data = {"data": row}
            return jsonify(response_data)

    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500



# CRUD OPERATIONS

# CREATE KEAGIATAN
# @kegiatan_api.route('/api/kegiatan', methods=['POST'])
# def createKegiatan():
#     try:
#         _json = request.json
#         _nama_kegiatan = _json['nama_kegiatan']
#         _tanggal = _json['tanggal']
#         _jam_mulai = _json['jam_mulai']
#         _jam_selesai = _json['jam_selesai']
#         _zona_waktu = _json['zona_waktu']
#         _tempat = _json['tempat']
#         _status = _json['status']
#         _is_draft = _json['is_draft']

#         #log data type
#         print(type(_json['is_draft']))

#         if _nama_kegiatan and _tanggal and _jam_mulai and _jam_selesai and _zona_waktu and _tempat and _status and _is_draft and request.method == 'POST':			
#             sqlQuery = "INSERT INTO kegiatan(nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
#             bindData = (_nama_kegiatan, _tanggal, _jam_mulai, _jam_selesai, _zona_waktu, _tempat, _status, _is_draft)            
#             conn = psycopg2.connect(**db_params)
#             cursor = conn.cursor()
#             cursor.execute(sqlQuery, bindData)
#             conn.commit()
            
#             respone = jsonify('Kegiatan berhasil ditambahkan!'), 200
#             return respone
#         else:
#             return jsonify({"message": "Uh oh, Data gagal disimpan!"}), 500
#     except (Exception, psycopg2.DatabaseError) as error:
#         # Create a custom error message
#         error_message = {"Oops, there's an error.. ": str(error)}
#         return jsonify(error_message), 500

# CANCEL KEGIATAN (SET STATUS TO BATAL)
@kegiatan_api.route('/api/kegiatan/batal', methods=['POST'])
def cancelKegiatan():
    try:
        _id = request.json['id_kegiatan']
        if _id and request.method == 'POST':			
            sqlQuery = "UPDATE kegiatan SET status = 'BATAL' WHERE id = %s"
            bindData = (_id,)            
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Kegiatan berhasil dibatalkan!')
            respone.status_code = 200
            return respone
        else:
            return jsonify({"message": "Uh oh, Ada kesalahan!"}), 500
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500
    
# UPDATE KEGIATAN by ID
@kegiatan_api.route('/api/kegiatan/<int:id>', methods=['PUT'])
def updateKegiatan(id):
    try:
        _json = request.json
        print("_json:", _json)  # Add debugging statement
        print("Data type of _json:", type(_json))
        
        _nama_kegiatan = _json['nama_kegiatan']
        _tanggal = _json['tanggal']
        _jam_mulai = _json['jam_mulai']
        _jam_selesai = _json['jam_selesai']
        _zona_waktu = _json['zona_waktu']
        _tempat = _json['tempat']
        _status = _json['status']
        _is_draft = _json['is_draft']
        # Check the data type of specific values
        nama_kegiatan_type = type(_json['nama_kegiatan'])
        tanggal_type = type(_json['tanggal'])
        jam_mulai_type = type(_json['jam_mulai'])
        jam_selesai_type = type(_json['jam_selesai'])
        zona_waktu_type = type(_json['zona_waktu'])
        tempat_type = type(_json['tempat'])
        status_type = type(_json['status'])
        is_draft_type = type(_json['is_draft'])

        # Print the data types
        print("nama_kegiatan_type:", nama_kegiatan_type)
        print("tanggal_type:", tanggal_type)
        print("jam_mulai_type:", jam_mulai_type)
        print("jam_selesai_type:", jam_selesai_type)
        print("zona_waktu_type:", zona_waktu_type)
        print("tempat_type:", tempat_type)
        print("status_type:", status_type)
        print("is_draft_type:", is_draft_type)
        if _nama_kegiatan and _tanggal and _jam_mulai and _jam_selesai and _zona_waktu and _tempat and _status and _is_draft and request.method == 'PUT':			
            sqlQuery = "UPDATE kegiatan SET nama_kegiatan=%s, tanggal=%s, jam_mulai=%s, jam_selesai=%s, zona_waktu=%s, tempat=%s, status=%s, is_draft=%s WHERE id=%s"
            bindData = (_nama_kegiatan, _tanggal, _jam_mulai, _jam_selesai, _zona_waktu, _tempat, _status, _is_draft, (id,))            
            conn = psycopg2.connect(**db_params)
            cursor = conn.cursor()
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Kegiatan berhasil diupdate!')
            respone.status_code = 200
            return respone
        else:
            return jsonify({"message": "Uh oh, Ada kesalahan!. Gagal Mengupdate Data."}), 500
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500



# DELETE KEGIATAN by ID
@kegiatan_api.route('/api/kegiatan/<int:id>', methods=['DELETE'])
def hapusKegiatan(id):
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM kegiatan WHERE id =%s", (id,))
        conn.commit()
        respone = jsonify('Kegiatan berhasil dihapus!')
        respone.status_code = 200
        return respone
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500
    





# reusables functions insert
def insert_source(table_name, columns, values, data):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s'] * len(values))})"
        cur.execute(sql, data)

        conn.commit()
        print('Source image data successfully imported')
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

# resuables functions view
def select_data(table_name):
    try:
        conn = psycopg2.connect(**db_params)
        cur = conn.cursor()

        sql = f"SELECT * FROM {table_name}"
        cur.execute(sql)
        rows = cur.fetchall()
        if rows is None:
            # If no data found, return a "no record available" message
            return jsonify({"message": "Belum ada data "}), 404  # 404 indicates "Not Found"
        else:
            for row in rows:
                row['jam_mulai'] = row['jam_mulai'].strftime("%H:%M")
                row['jam_selesai'] = row['jam_selesai'].strftime("%H:%M")
            
            # Create a JSON response with a list of records
            response_data = {"data": rows}
            return jsonify(response_data)

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None  # Return None in case of an error
    


@kegiatan_api.route('/api/kegiatan', methods=['GET'])
def getKegiatan():
    data = kegiatan_db.selectAllData('kegiatan')
    
    if data != 200:
        return data  # Wrap the result in a JSON-friendly dictionary
    else:
        return jsonify({"message": "An error occurred while fetching data."}), 500
    
