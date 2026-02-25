# job_actions/create_job_handler.py
from utils.jenkins_connection import server,JENKINS_Url
from utils.response_utils import generate_response, error_response,elicit_slot_response

def create_job(jobname, github_url=""):
    github_url="https://github.com/gurukiran2805/lex"
    job_type = 'Pipeline'
    if job_type == 'Freestyle':
         server.create_job(jobname, jenkins.EMPTY_CONFIG_XML)
    elif job_type == 'Pipeline':
         config_xml = """<flow-definition>
    <definition class="org.jenkinsci.plugins.workflow.cps.CpsFlowDefinition">
        <script>
            pipeline {
                agent any
                
                stages {
                    stage('First Stage') {
                        steps {
                            echo 'This is the first stage. Echoing a message.'
                        }
                    }
                    stage('Second Stage') {
                        steps {
                            echo 'Sleeping for 2 minutes in the second stage...'
                            // Sleep for 2 minutes
                            sleep 120
                        }
                    }
                }
                post {
                    always {
                        echo 'Build done!'
                    }
                }
            }
        </script>
    </definition>
</flow-definition>"""
         server.create_job(jobname, config_xml)
    #elif job_type == 'MultibranchPipeline' and github_url:
        # config_xml = f"""<flow-definition>
        #     <definition class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject">
        #         <sources>
        #             <jenkins.branch.GitHubSCMSource>
        #                 <repoOwner>my-repo-owner</repoOwner>
        #                 <repository>{github_url}</repository>
        #             </jenkins.branch.GitHubSCMSource>
        #         </sources>
        #     </definition>
        # </flow-definition>"""
        # server.create_job(jobname, config_xml)
    else:
        raise ValueError("Unsupported job type or missing GitHub URL")


def validate(slots):
    if not slots['JobName']:
        return {
          'isValid': False,
          'violatedSlot': 'JobName'
        }
    return {'isValid': True}

def create_job_handler(event):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    
    #jobname = slots['JobName']['value']['originalValue']
    #job_type = slots['JobType']['value']['originalValue']
    #github_url = slots.get('GitHubURL', {}).get('value', {}).get('originalValue', '')
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
        if server.job_exists(jobname):  
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
                        "content": f'JobName "{jobname}" is already present. Please try again with a valid job name.'
                    },
                    {
                        "contentType": "ImageResponseCard",
                        "content": " ",
                        "imageResponseCard": {
                        "title": " ",
                        "subtitle": f'JobName "{jobname}" is already present. Please try again with a valid job name.',
                        "buttons": [
                         {
                            "text": "Trigger build ",
                            "value":"trigger build "
                         },
                         {
                            "text": "Build Job",
                            "value":"Build job"
                         }
                         ]
                        }
                    }
                ]
            }
        
        else:
            try:
                
                result = create_job(jobname)
                message = (
                    f"🎉 **Success!** You've successfully created the  job: '{jobname}'.\n\n"
                    f"👉 You can now start building this job or manage it further.\n\n"
                    f"🔗 {JENKINS_Url}job/{jobname}"
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
                    f"❌ **Oops! Something went wrong** while creating the job.\n\n"
                    f"Error: {str(e)}. Please check the job type or GitHub URL and try again."
                )
