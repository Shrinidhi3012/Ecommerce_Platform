from flask import Flask, jsonify,request
app = Flask(__name__)
orders = [
    {"order_id": 101, "product_id": 1, "quantity": 2},
    {"order_id": 102, "product_id": 2, "quantity": 1}
]
@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)
@app.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = {
        "order_id": len(orders) + 101,
        "product_id": data["product_id"],
        "quantity": data["quantity"]
    }
    orders.append(new_order)
    return jsonify(new_order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)