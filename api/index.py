import json
import os

def handler(request):
    try:
        # Load the data from JSON file in the same directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(current_dir, "q-vercel-python.json")

        with open(json_file, "r") as f:
            data_list = json.load(f)

        data = {entry["name"]: entry["marks"] for entry in data_list}

        # Extract query params
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

        # Ensure it's a list
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
            "body": json.dumps({"error": "Internal Server Error", "details": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

handler.__name__ = "handler"  # VERY IMPORTANT for Vercel
