import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
        order_id = body["order_id"]

        table.delete_item(Key={"order_id": order_id})

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Order {order_id} deleted"})
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}