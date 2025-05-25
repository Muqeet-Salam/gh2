import json
import os

def handler(request):
    try:
        # Load the JSON file from the same folder
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "q-vercel-python.json")

        with open(json_path, "r") as f:
            data_list = json.load(f)

        # Convert to dictionary for quick lookup
        data = {entry["name"]: entry["marks"] for entry in data_list}

        # Get query parameters
        query = request.get("queryStringParameters", {})
        names = query.get("name")

        if not names:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No name parameters provided"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        # Normalize to list if single name
        if isinstance(names, str):
            names = [names]

        # Get marks in order
        marks = [data.get(name, 0) for name in names]

        return {
            "statusCode": 200,
            "body": json.dumps({"marks": marks}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET"
            }
        }

    except Exception as e:
        # Catch any error and return
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal Server Error", "details": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

handler.__name__ = "handler"
