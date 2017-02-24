import requests
import json

access_token = "access_token"
verify_token = "verify_token"

def send_message(send_id, msg_txt):

    params  = {"access_token": access_token}
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"recipient": {"id": send_id},
                       "message": {"text": msg_txt}})
                       
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)
        
def send_attachment(send_id, attach_url):
    params  = {"access_token": access_token}
    headers = {"Content-Type": "application/json"}
    data = json.dumps({"recipient": {
                        "id": send_id
                        },
                        "message": {
                            "attachment": {
                                "type": "image", 
                                "payload": {
                                    "url": attach_url, "is_reusable": True
                                }
                            }
                        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        print(r.status_code)
        print(r.text)


def lambda_handler(event, context):
    print(event)

    #process GET
    try:
        v_token = str(event[u'params'][u'querystring'][u'hub.verify_token'])
        challenge = str(event[u'params'][u'querystring'][u'hub.challenge'])
        if (verify_token == v_token):
            return(int(challenge))
    #process POST
    except:
        try:
            messaging_event = event['body-json']['entry'][0]['messaging'][0]
            if ("text" in messaging_event['message'].keys()):
                msg_txt   = messaging_event['message']['text']
                msg_atch  = "http://i.imgur.com/FbEhyWV.jpg"
                sender_id = messaging_event['sender']['id']
                send_message(sender_id, msg_txt)
                send_attachment(sender_id, msg_atch)
        except:
            print("we tried")
