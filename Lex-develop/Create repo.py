import requests
import config
from check_repo import check_repo_exists
from response import generate_response, error_response

def validate_create_repo(slots):
    if not slots.get('RepoName') or not slots['RepoName'].get('value', {}).get('originalValue'):
        return {
            'isValid': False,
            'violatedSlot': 'RepoName'
        }
    if not slots.get('techStack') or not slots['techStack'].get('value', {}).get('originalValue'):
        return {
            'isValid': False,
            'violatedSlot': 'techStack'
        }
    return {'isValid': True}

def create_repo_handler(event):
    slots = event['sessionState']['intent']['slots']
    intent_name = event['sessionState']['intent']['name']

    # DialogCodeHook: Handle the form elicitation if required
    if event['invocationSource'] == 'DialogCodeHook':
        validation_result = validate_create_repo(slots)
        if not validation_result['isValid']:
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "ElicitSlot",
                        "slotToElicit": validation_result['violatedSlot']
                    },
                    "intent": {
                        'name': intent_name,
                        'slots': slots
                    }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Let's create your repository! Please provide the following details."
                    }
                ],
                "responseCard": {
                    "version": 1,
                    "contentType": "Custom",
                    "content": {
                        "customPayload": {
                            "formType": "create_repo_form",
                            "fields": [
                                {
                                    "type": "Text",
                                    "label": "Repository Name",
                                    "name": "RepoName",
                                    "isRequired": True
                                },
                                {
                                    "type": "Dropdown",
                                    "label": "Tech Stack",
                                    "name": "techStack",
                                    "options": [
                                        {"label": "Node.js", "value": "node"},
                                        {"label": "Maven", "value": "maven"},
                                        {"label": "Python", "value": "python"}
                                    ],
                                    "isRequired": True
                                },
                                {
                                    "type": "Text",
                                    "label": "Repository Description",
                                    "name": "description",
                                    "isRequired": True
                                }
                            ],
                            "submitButtonLabel": "Submit"
                        }
                    }
                }
            }

        # If all required slots are filled, delegate the intent for fulfillment
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name': intent_name,
                    'slots': slots
                }
            }
        }

    # FulfillmentCodeHook: After form submission, process repository creation
    if event['invocationSource'] == 'FulfillmentCodeHook':
        repo_name = slots['RepoName']['value']['originalValue']
        tech_stack = slots['techStack']['value']['originalValue']
        description = slots.get('description', {}).get('value', {}).get('originalValue', "")

        try:
            # Check if repository already exists
            repo_exists, repo_url = check_repo_exists(repo_name)
            if repo_exists:
                return generate_response(
                    intent_name,
                    slots,
                    f"The repository **{repo_name}** already exists. You can access it here: {repo_url}",
                    state='Fulfilled'
                )

            # Create the repository on GitHub
            url = f"{config.GITHUB_API_URL}/user/repos"
            data = {
                "name": repo_name,
                "description": description,
                "private": False
            }
            headers = {
                "Authorization": f"token {config.GITHUB_TOKEN}"
            }
            response = requests.post(url, json=data, headers=headers)

            if response.status_code != 201:
                raise Exception(f"Failed to create repo: {response.json().get('message', 'Unknown error')}")

            repo_data = response.json()
            repo_url = repo_data.get("html_url")

            # Message to return after repo creation
            message = (
                f"The repository **{repo_name}** has been created.\n\n"
                f"📂 You can access it here: {repo_url}\n\n"
                f"A Jenkinsfile for **{tech_stack}** has also been added.\n\n"
                f"Would you like to create another repository or perform another action?"
            )

            return generate_response(intent_name, slots, message, state='Fulfilled')

        except Exception as e:
            return error_response(
                intent_name,
                slots,
                f"❌ **Repository Creation Failed**\n\n"
                f"Sorry, there was an issue while creating the repository: {str(e)}"
            )
