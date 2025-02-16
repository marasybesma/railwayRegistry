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

@app.route('/')
def getAll():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM items;")
            items = cursor.fetchall()

    response = jsonify(items)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/check/<int:id>')
def check(id: int):
    print(id)

    query = "UPDATE items SET checked = TRUE WHERE id = {0}".format(id)
    print(query)
    
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
        
        return jsonify({"success":True}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "oopsie woopsie! uwu we made a fucky wucky!! a wittle fucko boingo!"}), 404

@app.route('/uncheck/<int:id>')
def uncheck(id: int):
    print(id)

    query = "UPDATE items SET checked = FALSE WHERE id = {0}".format(id)
    print(query)
    
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query)
                
        return jsonify({"success":True}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "oopsie woopsie! uwu we made a fucky wucky!! a wittle fucko boingo!"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
