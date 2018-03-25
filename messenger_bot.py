# coding=UTF-8
import requests
import os
import sys
import json

def send_message(recipient_id, message_text, message_type="RESPONSE"):
    # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "messaging_type": message_type,
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.12/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


def send_image(recipient_id, url, message_type="RESPONSE"):
    # log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
    params = {
        "access_token": os.environ["PAGE_ACCESS_TOKEN"]
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "messaging_type": message_type,
        "recipient": {
            "id": recipient_id
        },
        "message":{
            "attachment":{
                "type":"image", 
                "payload":{
                    "url": url, 
                    "is_reusable":true
                }
            }
        }
    })
    r = requests.post("https://graph.facebook.com/v2.12/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)