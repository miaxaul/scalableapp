import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        order_id = str(uuid.uuid4())

        item = {
            "order_id": order_id,
            "customer_name": body["customer_name"],
            "food_item": body["food_item"],
            "quantity": body["quantity"]
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Order created", "order_id": order_id})
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}