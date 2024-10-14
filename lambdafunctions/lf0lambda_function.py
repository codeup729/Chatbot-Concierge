import json
import boto3
import uuid
from datetime import datetime

sessionId = "unique-user-id-123"
lex_client = boto3.client('lexv2-runtime')

def lambda_handler(event, context):
    
    body = event
    # Check if the messages key is present in the request
    if 'messages' in body:
        # Basic boilerplate response to return
        user_message = body['messages'][0]['unstructured']['text']
        response_message = "I'm still under development. Please come back later."

        lex_response = call_lex_bot(user_message)
        
        # Extract the response from Lex
        lex_message = lex_response['messages'][0]['content']

        current_timestamp = datetime.utcnow().isoformat() + 'Z'

        # Create a BotResponse object with a simple response
        bot_response = {
            "messages": [
                {
                    "type": "unstructured",
                    "unstructured": {
                        "id": "1",
                        "text": lex_message,
                        "timestamp": current_timestamp
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

def call_lex_bot(user_message):
    # Call the Lex bot using the Boto3 Lex V2 Runtime client
    response = lex_client.recognize_text(
        botId='LTMIBTN7U9',              # Replace with your Lex bot ID
        botAliasId='TSTALIASID',   # Replace with your Lex bot alias ID
        localeId='en_US',                 # Adjust if you're using a different locale
        sessionId=sessionId,      # Use a unique session ID for each user or conversation
        text=user_message                 # The user's message text
    )
    return response