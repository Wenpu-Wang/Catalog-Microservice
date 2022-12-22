import requests

from notification import NotificationMiddlewareHandler
from notification import format_message
from context import Context as context
import json

temp = {
    "blocks": [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "_You_ have a new request:\n*<fakeLink.toEmployeeProfile.com|Fred Enriquez - New device "
                        "request>* "
            }
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "*Type:*\nComputer (laptop)"
                },
                {
                    "type": "mrkdwn",
                    "text": "*When:*\nSubmitted Aut 10"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Last Update:*\nMar 10, 2015 (3 years, 5 months)"
                },
                {
                    "type": "mrkdwn",
                    "text": "*Reason:*\nAll vowel keys aren't working."
                },
                {
                    "type": "mrkdwn",
                    "text": "*Specs:*\n\"Cheetah Pro 15\" - Fast, really fast\""
                }
            ]
        },
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Approve"
                    },
                    "style": "primary",
                    "value": "click_me_123"
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "emoji": True,
                        "text": "Deny"
                    },
                    "style": "danger",
                    "value": "click_me_123"
                }
            ]
        }
    ]
}


def t_sns_1():
    NotificationMiddlewareHandler.get_sns_client()
    print("Got SNS Client!")
    tps = NotificationMiddlewareHandler.get_sns_topics()
    print("SNS Topics = \n", json.dumps(tps, indent=2))

    message = {"Name": "Wenpu Wang"}
    NotificationMiddlewareHandler.send_sns_message(
        sns_topic=context.get_context("SNS_ARN"),
        message=message
    )


def t_sns_notify():
    NotificationMiddlewareHandler.get_sns_client()
    print("Got SNS Client!")
    NotificationMiddlewareHandler.notify()


def t_slack():
    NotificationMiddlewareHandler.send_slack_message(
        "Cool", "Create",
        {
            "uni": "ww2569",
            "last_name": "Wenpu",
            "first_name": "Wang"
        }
    )


def t_format_message():
    resource_info = \
        {
            "uni": "ww2569",
            "last_name": "Wenpu999",
            "first_name": "Wang"
        }
    message = format_message(text_message="Resource Change",
                             event_type=None,
                             resource_info=resource_info
                             )
    slack_url = context.get_context("SLACK_URL")
    response = requests.post(
        slack_url, json=message,
        headers={'Content-Type': 'application/json'}
    )
    print(response.status_code)
    print("message:", message)


if __name__ == "__main__":
    # t_sns_1()
    t_slack()
    # t_format_message()
