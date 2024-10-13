import json

def lambda_handler(event, context):
    body = json.loads(event['messages'])

    # Check if the messages key is present in the request
    if 'messages' in body:
        # Basic boilerplate response to return
        response_message = "I'm still under development. Please come back later."

        # Create a BotResponse object with a simple response
        bot_response = {
            "messages": [
                {
                    "type": "text",
                    "unstructured": {
                        "id": "1",
                        "text": response_message,
                        "timestamp": "2024-10-12T18:00:00Z"
                    }
                }
            ]
        }

        # Return a response object that matches the BotResponse schema
        return {
            "statusCode": 200,
            "body": json.dumps(bot_response),
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            }
        }

    # In case the request does not contain 'messages', return a 400 error
    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Invalid BotRequest format."}),
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }