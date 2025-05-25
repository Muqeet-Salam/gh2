import json
import os

def handler(request):
    try:
        # Load the data file
        json_path = os.path.join(os.path.dirname(__file__), "q-vercel-python.json")
        with open(json_path, "r") as f:
            data_list = json.load(f)

        # Convert to dict for quick lookup
        data = {entry["name"]: entry["marks"] for entry in data_list}

        # Get query parameters
        params = request.get("queryStringParameters", {})
        names = params.get("name")

        if not names:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No name parameters provided"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        if isinstance(names, str):
            names = [names]

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
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

handler.__name__ = "handler"
