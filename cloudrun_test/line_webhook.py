import json
import os

import requests
from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot import WebhookHandler
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import MessagingApi

app = Flask(__name__)
load_dotenv()

URL = "https://api.line.me/v2/bot/message/push"

line_bot_api = MessagingApi(os.getenv('LINE_API_KEY'))
handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def send_message(message_text: str):
    line_api_key = os.getenv('LINE_API_KEY')
    user_id = os.getenv('LINE_MY_USER_ID')

    payload = json.dumps({
    "to": user_id,
    "messages": [
        {
        "type": "text",
        "text": message_text
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {line_api_key}'
    }

    requests.request("POST", URL, headers=headers, data=payload)
    return 'OK'


@app.route("/", methods=['POST', 'GET'])
def main():
    event = json.loads(request.get_data())
    message_data = event['events'][0]

    if message_data['message']['type'] == "text": 
        res_message = f'あなたは{message_data['message']['text']}と送ってきましたね！'
        send_message(res_message)
    elif message_data['message']['type'] == "audio": 
        send_message("audioが送信されました")
    else:
        send_message("サポートされていないフォーマットです")
        print("サポートされていないフォーマットです")
    
    return "hello"

if __name__ == "__main__":
    app.run(debug=True)
