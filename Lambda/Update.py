import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('Orders')

class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return int(o) if o % 1 == 0 else float(o)
        return super(DecimalEncoder, self).default(o)

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        order_id = body['order_id']
        customer_name = body['customer_name']
        food_item = body['food_item']
        quantity = body['quantity']

        response = table.update_item(
            Key={"order_id": order_id},
            UpdateExpression="SET customer_name = :c, food_item = :f, quantity = :q",
            ExpressionAttributeValues={
                ":c": customer_name,
                ":f": food_item,
                ":q": quantity
            },
            ReturnValues="ALL_NEW"
        )

        return {
            "statusCode": 200,
            "body": json.dumps(response['Attributes'], cls=DecimalEncoder)
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
