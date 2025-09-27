import json
import boto3
from decimal import Decimal
from flask import Flask, request, jsonify

app = Flask(__name__)

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table('Orders')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o) if o % 1 == 0 else float(o)
        return super(DecimalEncoder, self).default(o)

@app.route("/orders", methods=["GET"])
def get_orders():
    try:
        response = table.scan()
        orders = response.get("Items", [])
        return jsonify(orders)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/orders", methods=["POST"])
def add_order():
    try:
        data = request.get_json()
        table.put_item(Item=data)
        return jsonify({"message": "Order added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/orders/<order_id>", methods=["PUT"])
def update_order(order_id):
    try:
        data = request.get_json()
        table.update_item(
            Key={"orderId": order_id},
            UpdateExpression="set #n = :n, #q = :q",
            ExpressionAttributeNames={"#n": "name", "#q": "quantity"},
            ExpressionAttributeValues={":n": data["name"], ":q": data["quantity"]}
        )
        return jsonify({"message": "Order updated"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/orders/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    try:
        table.delete_item(Key={"orderId": order_id})
        return jsonify({"message": "Order deleted"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)