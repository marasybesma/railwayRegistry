from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

print("all environment variables")
print(os.environ)

connection = psycopg2.connect(
    host=os.environ.get("PGHOST"),
    user=os.environ.get("POSTGRES_USER"),
    password=os.environ.get("POSTGRES_PASSWORD"),
    port=int(os.environ.get("PGPORT"))
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
