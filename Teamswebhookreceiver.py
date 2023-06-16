"""
Copyright (c) 2023 Cisco and/or its affiliates.

This software is licensed to you under the terms of the Cisco Sample
Code License, Version 1.1 (the "License"). You may obtain a copy of the
License at

               https://developer.cisco.com/docs/licenses

All use of the material herein must be in accordance with the terms of
the License. All rights not expressly granted by the License are
reserved. Unless required by applicable law or agreed to separately in
writing, software distributed under the License is distributed on an "AS
IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied.

"""


import requests
import json
import os
import credentials
import mongodb_auth
from bson.objectid import ObjectId
from pprint import pprint


bot_email, bot_name = None, None
bearer = credentials.BOT_ACCESS_TOKEN

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json; charset=utf-8",
    "Authorization": "Bearer " + bearer
}


def send_webex_get(url, payload=None,js=True):
    if payload == None:
        request = requests.get(url, headers=headers)
    else:
        request = requests.get(url, headers=headers, params=payload)
    if js == True:
        request= request.json()
    return request

def send_webex_post(url, data):
    request = requests.post(url, json.dumps(data), headers=headers).json()
    return request

###########################################
# Bot Menu Section Below
###########################################

def main_menu(user_email):
    result = ""
    result = "Thank you for invoking me. I shall help you with the Cisco Cross-domain NOC for MSPs <br/>"\
            "Below are the commands that I understand:<br/>" \
            "`details <id>` - I will display the details of the requested dashboard entry.<br/>"
    return(result)



###########################################
# Bot User Function Section Below
###########################################

def greetings():
    return "Hello there, Welcome to the Cross-domain NOC for MSPs bot! I am here to help you with your Dashboard. Type 'help' to get the menu options"


def getdetails(roomid, id):
    db = mongodb_auth.authenticatedb(dbname='storedb')
    collection = db['store']
    if(ObjectId.is_valid(id)):
        result = collection.find_one(ObjectId(id))
        del result["_id"]
        text = "**Cross-domain NOC for MSPs** : https://charts.mongodb.com/charts-global-msp-noc-vktwd/public/dashboards/643d02a2-33ac-4db0-82cc-1e76be904285"
        send_webex_post("https://webexapis.com/v1/messages",
                                    {"roomId": roomid, "markdown": str(text)})
        for key,values in result.items():
            if(key=="alarm_summary" or key=="application_health_summary" or key=="device_health_summary" or key=="network_health_summary"):
                send_webex_post("https://webexapis.com/v1/messages",
                                    {"roomId": roomid, "markdown": "**"+str(key)+"** : "})
                send_webex_post("https://webexapis.com/v1/messages",
                                    {"roomId": roomid, "markdown": str(values)})
            else:
                send_webex_post("https://webexapis.com/v1/messages",
                                    {"roomId": roomid, "markdown": "**"+str(key)+"** : "})
                for key, v in values.items():
                    if(v!=[]):
                        text = "**"+key+"**" + " : "
                        send_webex_post("https://webexapis.com/v1/messages",
                                    {"roomId": roomid, "markdown": str(text)})
                        for item in v:
                            send_webex_post("https://webexapis.com/v1/messages",
                                    {"roomId": roomid, "markdown": str(item)})
    else:
        send_webex_post("https://webexapis.com/v1/messages",
                                {"roomId": roomid, "markdown": "provided ObjectId is not valid"})

###########################################
# Bot User Function Section Above
###########################################

def webex_webhook(request):
    if request.method == 'POST':
        webhook = request.get_json(silent=True)
        print("Webhook:",webhook)
        if webhook['resource'] == "memberships" and webhook['data']['personEmail'] == bot_email:
            send_webex_post("https://webexapis.com/v1/messages",
                            {
                                "roomId": webhook['data']['roomId'],
                                "markdown": (greetings() + "<br/>" + "**Note - if this is a group room, you have to mention me specifically with a \"@\" for me to respond**")
                            }
                            )
        msg = None
        if webhook['data']['personEmail'] != bot_email:
            user_email = webhook['data']['personEmail']
            result = send_webex_get(
                'https://webexapis.com/v1/messages/{0}'.format(webhook['data']['id']))
            in_message = result.get('text', '')
            if(webhook['data']['roomType'] != "direct"):
                in_message = in_message.split(' ', 1)[1]
###########################################
# Bot Menu to User Function Connector Section Below
###########################################  
            if(in_message.startswith("details") or in_message.startswith("Details") ) :
                in_message = in_message.split(' ', 1)[1]
                in_message = in_message.strip()
                print("got id:",in_message)
                msg = getdetails(roomid=webhook['data']['roomId'], id=in_message)
            else:
                msg = main_menu(user_email)
            if msg != None:
                send_webex_post("https://webexapis.com/v1/messages",
                                {"roomId": webhook['data']['roomId'], "markdown": msg})
        return "True"
    elif request.method == 'GET':
        message = "<center><img src=\"http://bit.ly/webexBot-512x512\" alt=\"webex Bot\" style=\"width:256; height:256;\"</center>" \
                  "<center><h2><b>Congratulations! Your <i style=\"color:#ff8000;\">%s</i> bot is up and running.</b></h2></center>" \
                  "<center><b><i>Please don't forget to create Webhooks to start receiving events from Cisco Webex!</i></b></center>" % bot_name
        return message

def runme(request):
    global bot_email, bot_name
    if len(bearer) != 0:
        test_auth = send_webex_get("https://webexapis.com/v1/people/me", js=False)
        if test_auth.status_code == 401:
            print("Looks like provided access token is not correct. \n"
                  "Please review it and make sure it belongs to your bot account.\n"
                  "Do not worry if you have lost the access token. "
                  "You can always go to https://developer.webex.com/apps.html "
                  "URL and generate a new access token.")
        elif test_auth.status_code == 200:
            test_auth = test_auth.json()
            bot_name = test_auth.get("displayName","")
            bot_email = test_auth.get("emails","")[0]
    else:
        print("'bearer' variable is empty! \n"
              "Please populate it with bot's access token and run the script again.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.webex.com/apps.html "
              "URL and generate a new access token.")
    if "@webex.bot" not in bot_email:
        print("your bot_email domain does not appear to be valid.\n"
              "Please review it and make sure it belongs to your bot account.\n"
              "Do not worry if you have lost the access token. "
              "You can always go to https://developer.webex.com/apps.html "
              "URL and generate a new access token.")
    else:
        return webex_webhook(request)