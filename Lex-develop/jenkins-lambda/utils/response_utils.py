def generate_response(intent, slots, message, state='Fulfilled'):
    """
    Generate a consistent response structure with message.
    """
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name': intent,
                'slots': slots,
                'state': state
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }

def error_response(intent, slots, error_message):
    """
    Handles error responses in a consistent manner.
    """
    return generate_response(
        intent,
        slots,
        f"❌ **Something went wrong**:\n\n{error_message}\n\nPlease try again later or contact support.",
        state='Failed'
    )

def elicit_slot_response(intent, slots, violated_slot, validation_result):
   
    if 'message' in validation_result:
        response = {
            "sessionState": {
                "dialogAction": {
                    'slotToElicit': validation_result['violatedSlot'],
                    "type": "ElicitSlot"
                },
                "intent": {
                    'name': intent,
                    'slots': slots
                }
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": validation_result['message']
                }
            ]
        }
    else:
        response = {
            "sessionState": {
                "dialogAction": {
                    'slotToElicit': validation_result['violatedSlot'],
                    "type": "ElicitSlot"
                },
                "intent": {
                    'name': intent,
                    'slots': slots
                }
            }
        }
    
    return response
