import requests
import pyimgur
import random
import json

access_token = ""
verify_token = ""

client_id     = ''
#client_secret = ''

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

def call_counter(func):
    def helper(*args, **kwargs):
        helper.calls += 1
        return func(*args, **kwargs)
    helper.calls = 0
    helper.__name__= func.__name__
    return helper
def memoize(func):
    mem = {}
    def memoizer(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in mem:
            mem[key] = func(*args, **kwargs)
        return mem[key]
    return memoizer
@call_counter
@memoize    
def levenshtein(s, t):
    if s == "":
        return len(t)
    if t == "":
        return len(s)
    if s[-1] == t[-1]:
        cost = 0
    else:
        cost = 1
    
    res = min([levenshtein(s[:-1], t)+1,
               levenshtein(s, t[:-1])+1, 
               levenshtein(s[:-1], t[:-1]) + cost])
    return res

def get_meme(client_id):
    im            = pyimgur.Imgur(client_id)
    memes_gallery = im.get_memes_gallery(limit=30)
    
    meme_urls = []
    for meme in memes_gallery:
        for image in meme.images:
            if not image.is_nsfw:
                meme_urls.append(image.link)
    
    out_url = random.sample(meme_urls, 1)[0]
    return(str(out_url))
    


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
                sender_id = messaging_event['sender']['id']
                if msg_txt.lower() == "meme":
                    meme_url = get_meme(client_id)
                    send_attachment(sender_id, meme_url)
                yeet_dist  = levenshtein(msg_txt.lower(), "yeet")
                return_txt = "'{text_echo}' has {lv_dist} yeet levels".format(text_echo=msg_txt[:50], lv_dist = yeet_dist)
                send_message(sender_id, return_txt)
        except:
            print("we tried")
