# job_actions/delete_job_handler.py
from utils.jenkins_connection import server,delete_job
from utils.response_utils import generate_response, error_response,elicit_slot_response

def validate(slots):
    if not slots['JobName']:
        return {
          'isValid': False,
          'violatedSlot': 'JobName'
        }
    return {'isValid': True}
    

def delete_job_handler(event):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    
    if event['invocationSource'] == 'DialogCodeHook':
        validation_result = validate(slots)  
        print("Validation Result:", validation_result)
        
        if not validation_result['isValid']:
            return elicit_slot_response(intent, slots, validation_result['violatedSlot'], validation_result)

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name': intent,
                    'slots': slots
                }
            }
        }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        jobname = slots['JobName']['value']['originalValue']
        if not server.job_exists(jobname):  
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        'name': intent,
                        'slots': slots,
                        'state': 'Fulfilled'
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": f'JobName "{jobname}" is not present. Please try again with a valid job name.'
                    }
                ]
            }
    
        try:
            result = delete_job(jobname)
            message = (
                f"🗑️ **Job Deleted!**\n\n"
                f"The Jenkins job **{jobname}** has been successfully deleted.\n\n"
                f"🔍 Do you want to create a new job, or perhaps build or manage an existing one?"
            )
            return generate_response(
                intent,
                slots,
                message,
                state='Fulfilled'
            )
        except Exception as e:
            return error_response(
                intent,
                slots,
                f"❌ **Deletion Failed**\n\n"
                f"Could not delete the job **{jobname}**. It might not exist or an error occurred.\n\n"
                f"Error: {str(e)}. Please check the job name and try again."
            )
