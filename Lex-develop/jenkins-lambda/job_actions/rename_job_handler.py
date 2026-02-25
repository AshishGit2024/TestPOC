# job_actions/rename_job_handler.py
from utils.jenkins_connection import server,JENKINS_Url
from utils.response_utils import generate_response, error_response,elicit_slot_response

def rename_job(old_jobname, new_jobname):
    if server.job_exists(old_jobname):
       job_config = server.get_job_config(old_jobname)
       server.create_job(new_jobname, job_config)
       server.delete_job(old_jobname)
       return True
    else:
        raise ValueError(f"Job '{old_jobname}' does not exist.")

def validate(slots):
    if not slots['JobName']:
        return {
          'isValid': False,
          'violatedSlot': 'JobName'
        }
    if not slots['NewJobName']:
        return {
          'isValid': False,
          'violatedSlot': 'NewJobName'
        }
    return {'isValid': True}

def rename_job_handler(event):
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
        # Check if the job exists before proceeding
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
            old_jobname = slots['JobName']['value']['originalValue']
            new_jobname = slots['NewJobName']['value']['originalValue']
            result = rename_job(old_jobname, new_jobname)
            message = (
                f"✂️ **Job Renamed!**\n\n"
                f"The Jenkins job **{old_jobname}** has been successfully renamed to **{new_jobname}**.\n\n"
                f"🔗 You can access the renamed job here: [New Job URL]({JENKINS_Url}job/{new_jobname}).\n\n"
                f"Would you like to take further action?"
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
                f"❌ **Rename Failed**\n\n"
                f"Could not rename the job **{old_jobname}**. It might not exist or an error occurred.\n\n"
                f"Error: {str(e)}. Please check the job name and try again."
            )
