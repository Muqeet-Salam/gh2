import json

def handler(request):
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Hello from index.py!"}),
        "headers": {
            "Content-Type": "application/json"
        }
    }


handler.__name__ = "handler"

