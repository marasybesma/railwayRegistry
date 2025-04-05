from flask import Flask, jsonify, request
import psycopg2
import os
import datetime

app = Flask(__name__)

connection = psycopg2.connect(
    host=os.environ.get("PGHOST"),
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    port=int(os.environ.get("PGPORT")),
    database=os.environ.get("PGDATABASE")
)

def log(action, id, ip, user_agent):
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM items WHERE id = %s;", id)
                print("{date} | {action} id {id} ({name}) | IP: {ip} } USER-AGENT: {user_agent}".format(
                    date = datetime.datetime.now(),
                    action = action,
                    name = cursor.fetchall()[0][1],
                    id = id,
                    user_agent = user_agent
                ))
                
    except Exception as e:
        print(e)

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
    log("CHECKED", id, request.remote_addr, request.user_agent)
    query = "UPDATE items SET checked = TRUE WHERE id = %s AND NOT locked"
    
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id))
        
        return jsonify({"success":True}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "oopsie woopsie! uwu we made a fucky wucky!! a wittle fucko boingo!"}), 404

@app.route('/uncheck/<int:id>')
def uncheck(id: int):
    log("UNCHECKED", id, request.remote_addr, request.user_agent)
    query = "UPDATE items SET checked = FALSE WHERE id = %s AND NOT locked"
    
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(query, (id))
                
        return jsonify({"success":True}), 200

    except Exception as e:
        print(e)
        return jsonify({"error": "oopsie woopsie! uwu we made a fucky wucky!! a wittle fucko boingo!"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
