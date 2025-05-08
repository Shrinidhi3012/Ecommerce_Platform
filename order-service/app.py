from flask import Flask, jsonify, request
import psycopg2
import os

app = Flask(__name__)

# Database connection details
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

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    product_id = data['product_id']
    quantity = data['quantity']

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO orders (product_id, quantity) VALUES (%s, %s) RETURNING order_id;",
        (product_id, quantity)
    )
    order_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "order_id": order_id,
        "product_id": product_id,
        "quantity": quantity
    }), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT order_id, product_id, quantity FROM orders;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    orders = [
        {"order_id": row[0], "product_id": row[1], "quantity": row[2]}
        for row in rows
    ]
    return jsonify(orders)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
