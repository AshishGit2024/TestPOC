from utils.jenkins_connection import server
from utils.response_utils import generate_response, error_response, elicit_slot_response 

def build_job(jobname):
    if server.job_exists(jobname):
        return server.build_job(jobname)
    else:
        raise ValueError(f"Job '{jobname}' does not exist.")


def validate(slots):
    if not slots['JobName']:
        return {
          'isValid': False,
          'violatedSlot': 'JobName'
        }
    return {'isValid': True}


def build_job_handler(event):
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
            build_url = build_job(jobname)  
            
            message = (
                f"🚀 **Build triggered!**\n\n"
                f"The build for job **{jobname}** has started successfully.\n\n"
                f"🔗 You can track the progress and see results here: {build_url}\n\n"
                f"Would you like to do anything else with this job"
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
                f"❌ **Build Failed**\n\n"
                f"Sorry, there was an error while triggering the build for **{jobname}**.\n\n"
                f"Error: {str(e)}. Please check the job name or try again later."
            )



