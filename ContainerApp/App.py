import json
import boto3
from decimal import Decimal
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")

dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table('Orders')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o) if o % 1 == 0 else float(o)
        return super().default(o)

# Serve frontend
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# GET all orders
@app.route("/orders", methods=["GET"])
def get_orders():
    response = table.scan()
    return jsonify(response.get("Items", []))

# POST create order
@app.route("/orders", methods=["POST"])
def add_order():
    data = request.get_json()
    table.put_item(Item={
        "order_id": data.get("order_id", str(len(data))),  # auto or from client
        "customer_name": data["customer_name"],
        "food_item": data["food_item"],
        "quantity": data["quantity"]
    })
    return jsonify({"message": "Order added"}), 201

# PUT update order
@app.route("/orders/<order_id>", methods=["PUT"])
def update_order(order_id):
    data = request.get_json()
    update_expr = "SET customer_name = :c, food_item = :f, quantity = :q"
    table.update_item(
        Key={"order_id": order_id},
        UpdateExpression=update_expr,
        ExpressionAttributeValues={
            ":c": data["customer_name"],
            ":f": data["food_item"],
            ":q": data["quantity"]
        }
    )
    return jsonify({"message": "Order updated"}), 200

# DELETE order
@app.route("/orders/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    table.delete_item(Key={"order_id": order_id})
    return jsonify({"message": "Order deleted"}), 200

# Health check
@app.route("/health", methods=["GET"])
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)   # ✅ ganti ke 80
