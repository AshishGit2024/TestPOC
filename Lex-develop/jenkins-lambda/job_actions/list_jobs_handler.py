# list_jobs_handler.py
from utils.jenkins_connection import server
from utils.response_utils import generate_response, error_response

def list_jobs():
    try:
        jobs = server.get_all_jobs() 
        if jobs:
            job_list_message = "\n".join([job['name'] for job in jobs])  
            return job_list_message
        else:
            return "No jobs are available at the moment."
    except Exception as e:
        raise ValueError(f"Error while retrieving jobs: {str(e)}")

def list_jobs_handler(event):
    intent = event['sessionState']['intent']['name']
    
    if event['invocationSource'] == 'DialogCodeHook':
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name': intent
                }
            }
        }

    if event['invocationSource'] == 'FulfillmentCodeHook':
        try:
            jobs = list_jobs()  # Get the list of jobs
            message = f"Here are the jobs available:\n\n{jobs}\n\nWould you like to perform any action on one of these jobs?"
            return generate_response(intent, {}, message, state='Fulfilled')
        except Exception as e:
            return error_response(
                intent,
                {},
                f"❌ **Failed to retrieve jobs**\n\nError: {str(e)}. Please try again later."
            )
