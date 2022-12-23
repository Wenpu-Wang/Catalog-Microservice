import os
import requests
import json
import boto3
from middleware.context import Context as context

AWSAccessKeyId = os.environ.get("AWSAccessKeyId")
AWSSecretKey = os.environ.get("AWSSecretKey")

"""
# Set the webhook_url to the one provided by Slack when you create the webhook at
https://my.slack.com/services/new/incoming-webhook/
webhook_url = 'https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX'
slack_data = {'text': "Sup! We're hacking shit together @HackSussex :spaghetti:"}

response = requests.post(
    webhook_url, data=json.dumps(slack_data),
    headers={'Content-Type': 'application/json'}
)
if response.status_code != 200:
    raise ValueError(
        'Request to slack returned an error %s, the response is:\n%s'
        % (response.status_code, response.text)
    )
"""


def format_message(text_message, event_type, resource_info):
    a_message = {
        "text": "*" + text_message + "*",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*Catalog Item Info Changed:*"
                }
            }
        ]
    }

    for k, v in resource_info.items():
        a_message["blocks"].append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": k + ":\t" + str(v)
                }
            }
        )

    return a_message


class NotificationMiddlewareHandler:
    sns_client = None

    def __init__(self):
        pass

    @classmethod
    def get_sns_client(cls):

        if NotificationMiddlewareHandler.sns_client is None:
            NotificationMiddlewareHandler.sns_client = sns = boto3.client(
                service_name="sns",
                region_name="us-east-1",
                aws_access_key_id=AWSAccessKeyId,
                aws_secret_access_key=AWSSecretKey,
            )
        return NotificationMiddlewareHandler.sns_client

    @classmethod
    def get_sns_topics(cls):
        s_client = NotificationMiddlewareHandler.get_sns_client()
        result = response = s_client.list_topics()
        topics = result["Topics"]
        return topics

    @classmethod
    def send_sns_message(cls, sns_topic, message):
        import json
        import boto3

        s_client = NotificationMiddlewareHandler.get_sns_client()
        response = s_client.publish(
            TargetArn=sns_topic,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
        print("Publish response = ", json.dumps(response, indent=2))

    @staticmethod
    def notify(request, response):

        subscriptions = context.get_context("SUBSCRIPTIONS")

        if request.path in subscriptions:

            notification = {}

            try:
                request_data = request.get_json()
            except Exception as e:
                request_data = None

            path = request.path

            if request.method == 'POST':
                notification["change"] = "CREATED"
                notification['new_state'] = request_data
                notification['params'] = path
            elif request.method == 'PUT':
                notification["change"] = "UPDATE"
                notification['new_state'] = request_data
                notification["params"] = path
            elif request.method == "DELETE":
                notification["change"] = "DELETED"
                notification["params"] = path
            else:
                notification = None

            slack_url = os.environ.get("SLACK_URL")

            if notification.get("change", None):
                print("notification", notification)
                request_data = json.dumps(notification)
                request_data = json.dumps({'text': request_data}).encode('utf-8')
                response = requests.post(
                    slack_url, data=request_data,
                    headers={'Content-Type': 'application/json'}
                )
                print("Respose = ", response.status_code)

    @staticmethod
    def send_slack_message(message, event_type, resource_info):

        s_url = os.environ.get("SLACK_URL")

        msg = format_message(message, event_type, resource_info)
        msg = json.dumps(msg).encode('utf-8')

        response = requests.post(
            s_url, data=msg,
            headers={'Content-Type': 'application/json'}
        )
        print("Respose = ", response.status_code)
