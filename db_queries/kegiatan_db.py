from flask import jsonify
from config import db_params
import psycopg2
import psycopg2.extras

# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# universal select all table

def selectAllData(table):
    try:
        cur.execute(f"SELECT * FROM {table} ORDER BY id ASC")
        rows = cur.fetchall()
        if rows is None:
            # If no data found, return a "no record available" message
            return jsonify({"message": "Data masih kosong!"}), 200  
        else:
            # If data found, return the user data
            for row in rows:
                row['jam_mulai'] = row['jam_mulai'].strftime("%H:%M")
                row['jam_selesai'] = row['jam_selesai'].strftime("%H:%M")
            
            # Create a JSON response with a list of records
            response_data = {"data": rows}
            return jsonify(response_data), 200
            # return jsonify({"data": rows}), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500


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
