from flask import Flask, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "postgres")
DB_NAME = os.environ.get("DB_NAME", "ecommerce")
DB_USER = os.environ.get("DB_USER", "ecommerce_user")
DB_PASS = os.environ.get("DB_PASS", "secret123")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT product_id, name, price FROM products;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    products = [
        {"id": row[0], "name": row[1], "price": float(row[2])}
        for row in rows
    ]
    return jsonify(products)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
