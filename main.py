from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

connection = psycopg2.connect(
    host="${{Postgres.PGUSER}}",
    user="${{Postgres.POSTGRES_USER}}",
    password="${{Postgres.POSTGRES_PASSWORD}}",
    port="${{Postgres.PGPORT}}"
)

@app.route('/')
def index():
    with connection:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM items;")
            items = cursor.fetchall()
    return jsonify(items)


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
