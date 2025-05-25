import json
import os

def handler(request):
    try:
        print("Received request:", request)

        # Get the absolute path to the JSON file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "q-vercel-python.json")

        # Load JSON data
        with open(json_path, "r") as f:
            data_list = json.load(f)

        # Convert to dictionary
        data = {entry["name"]: entry["marks"] for entry in data_list}
        print("Data dictionary:", data)

        # Extract query params
        query_params = request.get("queryStringParameters", {})
        names = query_params.get("name")

        # Handle missing names
        if not names:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No name parameters provided"}),
                "headers": {
                    "Content-Type": "application/json",
                    "Access-Control-Allow-Origin": "*"
                }
            }

        # Normalize to list
        if isinstance(names, str):
            names = [names]

        print("Names:", names)

        # Get marks
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
        # Print error and return 500
        print("Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error", "details": str(e)}),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

handler.__name__ = "handler"



