from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

connection = psycopg2.connect(
    host=os.environ.get("PGHOST"),
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    port=int(os.environ.get("PGPORT")),
    database=os.environ.get("PGDATABASE")
)

def sortByPrice(e):
    return e[4]

@app.route('/')
def getAll():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM items;")
            items = cursor.fetchall().sort(key=sortByPrice)
    return jsonify(items)

@app.route('/check/<int:id>')
def check(id: int):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("UPDATE items SET checked = TRUE WHERE id = {id}" )
                
        return jsonify({"success":True}), 200

    except:
        return jsonify({"error": "oopsie woopsie! uwu we made a fucky wucky!! a wittle fucko boingo!"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
