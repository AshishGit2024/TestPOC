from job_actions.create_job_handler import create_job_handler
from job_actions.build_job_handler import build_job_handler
from job_actions.delete_job_handler import delete_job_handler
from job_actions.rename_job_handler import rename_job_handler
from job_actions.abort_job_handler import abort_job_handler
from job_actions.list_jobs_handler import list_jobs_handler 
from job_actions.greet_job_handler import greet_job_handler  
from utils.response_utils import error_response
from utils.fallback import fallback_handler
 
def lambda_handler(event, context):
   
    print(f"Received event: {event}")
    
    intents = event['sessionState']['intent']['name']
    
    if intents == 'CreateJobIntent':
        return create_job_handler(event)
    elif intents == 'BuildJobIntent':
        return build_job_handler(event)
    elif intents == 'DeleteJobIntent':
        return delete_job_handler(event)
    elif intents == 'RenameJobIntent':  
        return rename_job_handler(event)
    elif intents == 'AbortJobIntent':  
        return abort_job_handler(event)
    elif intents == 'ListJobsIntent':  
       return list_jobs_handler(event)
    elif intents == 'GreetJobIntent':  
        return greet_job_handler(event)
    elif intents == 'FallbackIntent':
        return fallback_handler(event)
    else:
        error_message = "Unrecognized intent detected."  
        return error_response(
            intent=intents,
            slots={},  
            error_message=error_message  
        )
