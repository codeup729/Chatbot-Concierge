import json

def lambda_handler(event, context):
    # Extract intent and slots from Lex V2 event
    intent_name = event['sessionState']['intent']['name']
    slots = event['sessionState']['intent']['slots']
    invocation_source = event['invocationSource']

    if intent_name == "GreetingIntent":
        return close(
            session_attributes=event['sessionState'].get('sessionAttributes', {}),
            fulfillment_state='Fulfilled',
            message={'contentType': 'PlainText', 'content': 'Hi there! How can I help you today?'}
        )

    elif intent_name == "ThankYouIntent":
        return close(
            session_attributes=event['sessionState'].get('sessionAttributes', {}),
            fulfillment_state='Fulfilled',
            message={'contentType': 'PlainText', 'content': "You're welcome!"}
        )

    elif intent_name == "DiningSuggestionsIntent":
        if invocation_source == 'DialogCodeHook':
            # Perform validation or slot elicitation
            validation_result = validate_dining_suggestions(slots)
            if not validation_result['isValid']:
                return elicit_slot(
                    session_attributes=event['sessionState'].get('sessionAttributes', {}),
                    intent_name=intent_name,
                    slots=slots,
                    slot_to_elicit=validation_result['violatedSlot'],
                    message={'contentType': 'PlainText', 'content': validation_result['message']}
                )
            # If all slots are valid, delegate to Lex to prompt for next slot
            return delegate(
                session_attributes=event['sessionState'].get('sessionAttributes', {}),
                slots=slots
            )
        elif invocation_source == 'FulfillmentCodeHook':
            # Fulfill the intent after all slots are filled
            response_message = (
                f"I see you're looking for {slots['Cuisine']['value']['interpretedValue']} restaurants "
                f"in {slots['Location']['value']['interpretedValue']} for {slots['NumberOfPeople']['value']['interpretedValue']} "
                f"people at {slots['DiningTime']['value']['interpretedValue']}. "
                f"I'll send the suggestions to {slots['Email']['value']['interpretedValue']}."
            )
            return close(
                session_attributes=event['sessionState'].get('sessionAttributes', {}),
                fulfillment_state='Fulfilled',
                message={'contentType': 'PlainText', 'content': response_message}
            )

    else:
        return close(
            session_attributes=event['sessionState'].get('sessionAttributes', {}),
            fulfillment_state='Failed',
            message={'contentType': 'PlainText', 'content': "Sorry, I didn't understand that. Can you please rephrase?"}
        )

def validate_dining_suggestions(slots):
    # Implement slot validation logic
    required_slots = ['Location', 'Cuisine', 'DiningTime', 'NumberOfPeople', 'Email']
    for slot in required_slots:
        if slots.get(slot) is None or slots[slot].get('value') is None:
            return {
                'isValid': False,
                'violatedSlot': slot,
                'message': f"Please provide {slot}."
            }
    # All slots are valid
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
