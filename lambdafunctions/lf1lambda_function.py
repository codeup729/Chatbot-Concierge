import json
import boto3
import os

# Initialize SQS client
sqs = boto3.client('sqs')

# Your SQS Queue URL (Q1)
SQS_QUEUE_URL = os.environ.get('SQS_QUEUE_URL', 'https://sqs.us-east-1.amazonaws.com/054037138954/DiningSuggestionsQueue-Q1')

def lambda_handler(event, context):
    intent_name = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    invocation_source = event['invocationSource']

    if intent_name == "DiningSuggestionsIntent":
        if invocation_source == 'DialogCodeHook':
            validation_result = validate_dining_suggestions(slots)
            if not validation_result['isValid']:
                return elicit_slot(
                    session_attributes=event['sessionState'].get('sessionAttributes', {}),
                    intent_name=intent_name,
                    slots=slots,
                    slot_to_elicit=validation_result['violatedSlot'],
                    message={'contentType': 'PlainText', 'content': validation_result['message']}
                )
            return delegate(
                session_attributes=event['sessionState'].get('sessionAttributes', {}),
                slots=slots
            )
        elif invocation_source == 'FulfillmentCodeHook':
            # Collect user information from slots
            location = slots['Location']['value']['interpretedValue']
            cuisine = slots['Cuisine']['value']['interpretedValue']
            dining_time = slots['DiningTime']['value']['interpretedValue']
            number_of_people = slots['NumberOfPeople']['value']['interpretedValue']
            email = slots['Email']['value']['interpretedValue']

            # Push information to SQS queue
            message_body = {
                "Location": location,
                "Cuisine": cuisine,
                "DiningTime": dining_time,
                "NumberOfPeople": number_of_people,
                "Email": email
            }

            # Send message to SQS
            response = sqs.send_message(
                QueueUrl=SQS_QUEUE_URL,
                MessageBody=json.dumps(message_body)
            )

            response_message = (f"I see you're looking for {cuisine} restaurants in {location} "
                                f"for {number_of_people} people at {dining_time}. "
                                f"I will send the suggestions to {email} and the details have been added to the queue.")

            return close(
                session_attributes=event['sessionState'].get('sessionAttributes', {}),
                fulfillment_state='Fulfilled',
                message={'contentType': 'PlainText', 'content': response_message}
            )

    else:
        return close(
            session_attributes=event['sessionState'].get('sessionAttributes', {}),
            fulfillment_state='Failed',
            message={'contentType': 'PlainText', 'content': "Sorry, I didn't understand that."}
        )

def validate_dining_suggestions(slots):
    required_slots = ['Location', 'Cuisine', 'DiningTime', 'NumberOfPeople', 'Email']
    for slot in required_slots:
        if slots.get(slot) is None or slots[slot].get('value') is None:
            return {
                'isValid': False,
                'violatedSlot': slot,
                'message': f"Please provide {slot}."
            }
    return {'isValid': True}

def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'ElicitSlot',
                'slotToElicit': slot_to_elicit
            },
            'intent': {
                'name': intent_name,
                'slots': slots,
                'state': 'InProgress'
            }
        },
        'messages': [message]
    }

def delegate(session_attributes, slots):
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Delegate'
            },
            'intent': {
                'name': 'DiningSuggestionsIntent',
                'slots': slots,
                'state': 'InProgress'
            }
        }
    }

def close(session_attributes, fulfillment_state, message):
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': {
                'name': 'DiningSuggestionsIntent',
                'state': fulfillment_state
            }
        },
        'messages': [message]
    }
