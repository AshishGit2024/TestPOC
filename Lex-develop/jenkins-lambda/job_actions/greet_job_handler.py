import random

def greet_job_handler(event):
    greetings = [
    "Hello! I'm JenkinsBot. How can I assist you today? Please select an option below to get started.",
    "Hi there! JenkinsBot here. What can I do for you today? Just choose an option to get started.",
    "Hello! JenkinsBot at your service. How can I help you today? Please select an option to proceed.",
    "Hi! I'm JenkinsBot. Ready to help with your Jenkins jobs. Please pick an option below to get started.",
    "Hey there! JenkinsBot here. What task can I assist you with today? Choose an option to continue.",
    "Hello! JenkinsBot here. How can I assist you today? Select an option below, and we’ll get going."
]

    selected_greeting = random.choice(greetings)


    response = {
        "sessionState": {
            "dialogAction": {
                "type": "ElicitIntent",  
                "message": {
                    "contentType": "PlainText",
                    "content": selected_greeting
                }
            },
            "intent": {
                "name": "GreetJobIntent",
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "ImageResponseCard",
                "content": " ",
                "imageResponseCard": {
                    "title": selected_greeting,
                    "subtitle": " ",
                    "buttons": [
                        {
                            "text": "Create Job",
                            "value":"Create job"
                        },
                        {
                            "text": "Build Job",
                            "value":"Build job"
                        },
                        {
                            "text": "Rename Job",
                            "value": "rename job"
                        },
                        {
                            "text": "Abort Job",
                            "value": "abort job"
                        },
                        {
                            "text": "Delete Job",
                            "value": "Delete job"
                        }
                    ]
                }
              }

        ]
    }

    return response
