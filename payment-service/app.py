from flask import Flask, jsonify, request
from prometheus_flask_exporter import PrometheusMetrics
import psycopg2
import os

app = Flask(__name__)
metrics = PrometheusMetrics(app)

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

@app.route('/payments', methods=['POST'])
def create_payment():
    data = request.get_json()
    order_id = data['order_id']
    amount = data['amount']
    status = "success"

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO payments (order_id, amount, status) VALUES (%s, %s, %s) RETURNING payment_id;",
        (order_id, amount, status)
    )
    payment_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "payment_id": payment_id,
        "order_id": order_id,
        "amount": amount,
        "status": status
    }), 201

@app.route('/payments', methods=['GET'])
def get_payments():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT payment_id, order_id, amount, status FROM payments;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    payments = [
        {"payment_id": row[0], "order_id": row[1], "amount": float(row[2]), "status": row[3]}
        for row in rows
    ]
    return jsonify(payments)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
