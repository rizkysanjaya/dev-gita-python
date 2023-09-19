from flask import jsonify
from config import db_params
import psycopg2
import psycopg2.extras


# db connect
conn = psycopg2.connect(**db_params)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# GET ALL z DATA
def selectAllData(table, condition=None):
    try:
        query = f"SELECT * FROM {table}"
        if condition:
            query += f" WHERE {condition}"
        query += " ORDER BY id ASC"
        # print(query)
        cur.execute(query)
        rows = cur.fetchall()

        if not rows:  # Check if rows is empty (no records found)
            # Return a "no record available" message
            response_data = {"message": "Data masih kosong!"}
            return jsonify(response_data), 200  # Use 404 to indicate "Not Found" 

        if table == 'kegiatan':
            for row in rows:
                row['jam_mulai'] = row['jam_mulai'].strftime("%H:%M")
                row['jam_selesai'] = row['jam_selesai'].strftime("%H:%M")


        # Create a JSON response with a list of records
        response_data = {"data": rows}
        return jsonify(response_data), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500

# reusable delete data function
def deleteData(table, id):
    try:
        query = f"DELETE FROM {table} WHERE id = {id}"
        cur.execute(query)
        conn.commit()
        response_data = {"message": "Data berhasil dihapus!"}
        return jsonify(response_data), 200
    except (Exception, psycopg2.DatabaseError) as error:
        # Create a custom error message
        error_message = {"Oops, there's an error.. ": str(error)}
        return jsonify(error_message), 500