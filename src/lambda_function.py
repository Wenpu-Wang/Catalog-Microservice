import urllib3
import json

http = urllib3.PoolManager()
slack_url = "https://hooks.slack.com/services/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"

# Formatt for slack
def format_message(text_message, event_type, resource_info):
    a_message = {
        "text": "*" + text_message + "*",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*New Item Info*"
                }
            }
        ]
    }

    print("in the format function!")
    print("resource_info type=", type(resource_info))
    
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

def lambda_handler(event, context):
    resource_info = json.loads(event["Records"][0]["Sns"]["Message"])

    # formatting for slack
    text = format_message(
        text_message="Resource Change",
        event_type=None,
        resource_info=resource_info
                         )
    
    text["username"] = "6156 Catalog Microservice Lambda Func"
    text["icon_url"] = "https://i.pinimg.com/originals/77/59/86/775986f65f43ba08ffbde1b9a55596bf.png"
    
    encoded_msg = json.dumps(text).encode("utf-8")
    resp = http.request("POST", slack_url, body=encoded_msg)
    print("status=", resp.status)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Test send message to Slack'),
    }
