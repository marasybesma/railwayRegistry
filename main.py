from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

print("DATABASE_URL")
print(os.environ.get("Postgres.DATABASE_URL"))

connection = psycopg2.connect(
    host=os.environ.get("Postgres.DATABASE_URL"),
    user=os.environ.get("Postgres.POSTGRES_USER"),
    password=os.environ.get("Postgres.POSTGRES_PASSWORD"),
    port=int(os.environ.get("Postgres.PGPORT"))
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
