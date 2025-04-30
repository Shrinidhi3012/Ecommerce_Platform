from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/products', methods=['GET'])
def get_products():
    return jsonify([
        {"id": 1, "name": "Cricket_Bat", "price": 1000},
        {"id": 2, "name": "Football", "price": 700}
    ])
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)