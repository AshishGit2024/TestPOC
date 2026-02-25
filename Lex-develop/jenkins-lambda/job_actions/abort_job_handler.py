from utils.jenkins_connection import server
from utils.response_utils import generate_response, error_response, elicit_slot_response 

    
def validate(slots):
    if not slots['JobName']:
        return {
          'isValid': False,
          'violatedSlot': 'JobName'
        }
    return {'isValid': True}

def abort_build_job(jobname):
    if server.job_exists(jobname):
        builds = server.get_job_info(jobname)['builds']
        for build in builds:
            build_number=build['number']
            build_info=server.get_build_info(jobname,build_number)
            if build_info['building']:
                return server.stop_build(jobname,build_number)
        raise ValueError(f"No running builds found for job '{jobname}'")
    else:
        raise ValueError(f"Job '{jobname}' does not exist.")

def abort_job_handler(event):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    
    if event['invocationSource'] == 'DialogCodeHook':
        validation_result = validate(slots)  
        
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
        try:
            abort_build_job(jobname)
            message = (
                f"🛑 **Build aborted!**\n\n"
                f"The build for job **{jobname}** has been successfully aborted.\n\n"
                f"Would you like to do anything else with this job?"
            )
            return generate_response(
                intent,
                slots,
                message,
                state='Fulfilled'
            )
        except ValueError as e:
            message = (
                f"🚫 **Build not found!**\n\n"
                f"No running build found for job **{jobname}**. Please try again later."
            )
            return generate_response(
                intent,
                slots,
                message,
                state='Fulfilled'
            )
        except Exception as e:
            message = (
                f"❌ **Build Failed!**\n\n"
                f"Sorry, there was an error while aborting the build for **{jobname}**.\n\n"
                f"Error: {str(e)}. Please check the job name or try again later."
            )
            return error_response(
                intent,
                slots,
                message
            )