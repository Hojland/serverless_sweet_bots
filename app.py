import jmespath
import requests
import json
from urllib.parse import unquote, parse_qs
import random
import re
from cowpy import cow

def insult(event, context):
    body = event['body']
    slack_event = {body_part.split('=')[0]: body_part.split('=')[1] for body_part in body.split('&')}

    url = "https://evilinsult.com/generate_insult.php?lang=en&type=json"
    res = requests.get(url).json()
    output = jmespath.search("insult", res)
    body = {"response_type": "in_channel", "text": output}
    #headers = {"X-Slack-No-Retry": "1", "Content-type": "application/json"}
    #r = requests.post(unquote(slack_event['response_url']), data=json.dumps(body))
    return {
            "statusCode": 200,
            "body": json.dumps(body)
            }

def praise(event, context):
    print(json.dumps(event))
    body = event['body']
    slack_event = {body_part.split('=')[0]: body_part.split('=')[1] for body_part in body.split('&')}

    url = "https://app.mikkomarttila.com/praise"
    output = requests.get(url).json()[0]
    body = {"response_type": "in_channel", "text": output}
    body = {"response_type": "in_channel", "text": output}
    #headers = {"X-Slack-No-Retry": "1", "Content-type": "application/json"}
    #r = requests.post(unquote(slack_event['response_url']), data=json.dumps(body))
    return {
            "statusCode": 200,
            "body": json.dumps(body)
            }

def compliment(event, context):
    print(json.dumps(event))
    body = event['body']
    slack_event = {body_part.split('=')[0]: body_part.split('=')[1] for body_part in body.split('&')}

    url = "https://complimentr.com/api"
    res = requests.get(url).json()
    output = jmespath.search("compliment", res)
    body = {"response_type": "in_channel", "text": output}
    #headers = {"X-Slack-No-Retry": "1", "Content-type": "application/json"}
    #r = requests.post(unquote(slack_event['response_url']), data=json.dumps(body))
    return {
            "statusCode": 200,
            "body": json.dumps(body)
            }

def hate(event, context):
    print(json.dumps(event))
    body = event['body']
    slack_event = {body_part.split('=')[0]: body_part.split('=')[1] for body_part in body.split('&')}

    url = 'https://insult.mattbas.org/api/insult'
    output = requests.get(url).text
    body = {"response_type": "in_channel", "text": output, "replace_original": "true"}
    #headers = {"X-Slack-No-Retry": "1", "Content-type": "application/json"}
    #r = requests.post(unquote(slack_event['response_url']), data=json.dumps(body))
    return {
            "statusCode": 200,
            "body": json.dumps(body)
            }

def cowsay(event, context):
    print(json.dumps(event))
    body = event['body']
    slack_event = parse_qs(body)
    print(slack_event)

    say_texts = open("nicolaiiversen", "r").read().split('\n%\n')
    i = random.choice(range(0, len(say_texts)))
    say_text = say_texts[i]

    if 'text' in slack_event.keys():
        input_text = slack_event['text'][0]
        quoted_name = re.findall('["“](.*?)["”]', input_text)
        say_text = say_text.replace('Nicolai Iversen', quoted_name[0])
        
    #cow_obj = cow.Moose(thoughts=True, tongue=True, eyes='dead')
    output = cow.milk_random_cow(say_text)

    body = {"response_type": "in_channel", "text": output, "delete_original": "true"}

    return {
            "statusCode": 200,
            "body": json.dumps(body)
            }

# We need a message to delete
#def delete_chat_message(slack_event: dict):
#    token = slack_event['token']
#    headers = {"X-Slack-No-Retry": "1", "Content-type": "application/json"}
#    body = {
#        "channel": slack_event['channel_id'],
#        "ts": "MESSAGE_TO_DELETE"
#        }
#    r = requests.post('https://slack.com/api/chat.delete', data=json.dumps(body))


POST https://slack.com/api/chat.delete
Content-type: application/json
Authorization: Bearer xoxb-your-token


#def send_slack_notice(response: str):
#    client_session = boto3.session.Session()
#    slack_token = get_secret(client_session)
#    slack_client = slack.WebClient(token=slack_token)
#
#    channel = '@molheh'
#    send_slack_message(slack_client, channel, response)
#    return {'status': 'SUCCESS'}
#
#def get_secret(client_session):
#    secret_name = "slack_api_token"
#    region_name = "eu-central-1"
#
#    # Create a Secrets Manager client
#    secrets_client = client_session.client(
#        service_name='secretsmanager',
#        region_name=region_name
#    )
#    resp = secrets_client.get_secret_value(SecretId=secret_name)
#    secret = resp['SecretString']
#    secret = json.loads(secret)
#    return secret['SLACK_API_TOKEN']
#
#
#def send_slack_message(slack_client, channel, message):
#  return slack_client.chat_postMessage(
#    channel=channel,
#    text=message
#  )