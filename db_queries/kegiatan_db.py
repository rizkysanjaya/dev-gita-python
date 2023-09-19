from flask import jsonify, request
from config import db_params
import psycopg2
import psycopg2.extras

# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# # Kegiatan Database Route

# Creaate kegiatan
def addKegiatan(values):
    try:
        placeholders = ', '.join(['%s'] * len(values))
        columns = 'nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft'
        sql = f"INSERT INTO kegiatan ({columns}) VALUES ({placeholders})"
        cur.execute(sql, values)
        # If the execution is successful, commit the transaction
        cur.connection.commit()
        return jsonify({"message": "Data kegiatan berhasil ditambahkan!"}), 200

    except psycopg2.Error as error:
        # Capture and log the actual error message from the database
        error_message = str(error)
        print("Database Error:", error_message)
        return jsonify({"message": "Data kegiatan gagal ditambahkan!", "Error Message": error_message}), 500
    
 
# Update kegiatan
def editKegiatan(values, id):
    try:
        
        # values = [nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft]
        placeholders = ', '.join(['%s'] * len(values))
        columns = 'nama_kegiatan, tanggal, jam_mulai, jam_selesai, zona_waktu, tempat, status, is_draft'

        # Update the record in the database
        sql = f"UPDATE kegiatan SET ({columns}) = ({placeholders}) WHERE id = {id}"
        cur.execute(sql, values)
        cur.connection.commit()
        return jsonify({"message": "Data kegiatan berhasil diupdate!"}), 200

    except psycopg2.Error as error:
        # Capture and log the actual error message from the database
        error_message = str(error)
        print("Database Error:", error_message)
        return jsonify({"message": "Data kegiatan gagal ditambahkan!", "Error Message": error_message}), 500

# Cancel kegiatan
def cancelKegiatan(id):
    try:
        query = f"UPDATE kegiatan SET status='BATAL' WHERE id={id}"
        cur.execute(query)
        cur.connection.commit()
        return jsonify({"message": "Data kegiatan berhasil dibatalkan!"}), 200
    except psycopg2.Error as error:
        # Capture and log the actual error message from the database
        error_message = str(error)
        print("Database Error:", error_message)
        return jsonify({"message": "Data kegiatan gagal dibatalkan!", "Error Message": error_message}), 500
        


# Delete kegiatan