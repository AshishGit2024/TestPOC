import random

def fallback_handler(event):
    print("Handling FallbackIntent...")

    fallback_messages = [
    "Sorry, I didn’t understand. Please try again, or contact DevOps support if the issue persists.",
    "I didn’t catch that. Please rephrase, or reach out to DevOps support if needed.",
    "There was an issue. Try again, or contact DevOps support for assistance.",
    "Apologies, I didn’t understand. Please try again or contact DevOps support if problems continue.",
    "Sorry, I missed that. Please retry, or contact DevOps support for further help."
    ]

    restart_help_messages = [
    "If you'd like to restart, type 'restart', or type 'help' for assistance.",
    "To begin again, type 'restart', or type 'help' for guidance.",
    "Type 'restart' to restart, or 'help' if you need more information.",
    "For a fresh start, type 'restart', or type 'help' if you need support.",
    "Type 'restart' to try again, or 'help' for assistance."
  ]


    # Randomly choose a greeting message
    selected_fallback = random.choice(fallback_messages)

    selected_help= random.choice(restart_help_messages)

    # Construct the response
    response = {
        "sessionState": {
                "dialogAction": {
                    "type": "ElicitIntent"
                },
                "intent": {
                    "name": "FallbackIntent",
                    "state": "Fulfilled"
                },
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": selected_fallback
                },
                {
                    "contentType": "ImageResponseCard",
                    "content": " ",
                    "imageResponseCard": {
                        "title": selected_help,
                        "subtitle": " ",
                        "buttons": [
                         {
                            "text": "help",
                             "value":"help"
                         },
                         {
                            "text": "restart",
                            "value":"restart"
                         }
                    ]
                  }
                }
            ]
    }

    return response
