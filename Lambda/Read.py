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
        response = table.scan()
        orders = response.get("Items", [])

        return {
            "statusCode": 200,
            "body": json.dumps(orders, cls=DecimalEncoder)  # pakai encoder
        }

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}