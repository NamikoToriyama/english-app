import json
import os
import logging

from dotenv import load_dotenv
from flask import Flask, abort, request
from linebot import WebhookHandler
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError


from const import MODEL, PROJECT_ID, PROMPT, URL
from lib import transcribe_by_speech_to_text, enhance_text_with_gemini, convert_to_wav, send_message, write_contents, output_file_name

app = Flask(__name__)

# ロギングの設定
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

load_dotenv()

handler = WebhookHandler(os.getenv('LINE_CHANNEL_SECRET'))

def audio_main(message_id: str):
    ### audioの取得
    write_contents(message_id)

    ### wavに変換
    convert_to_wav()

    ### 音声を文字にする
    speech_script = transcribe_by_speech_to_text(output_file_name)
    send_message(speech_script)

    ### GeminiAIでtextを添削する
    gemini_response = enhance_text_with_gemini(speech_script)
    send_message(gemini_response)


@app.route("/", methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return  "Get hello"
    
    event = json.loads(request.get_data())
    message_data = event['events'][0]

    if message_data['message']['type'] == "text": 
        res_message = f"あなたは{message_data['message']['text']}と送ってきましたね！"
        send_message(res_message)
    elif message_data['message']['type'] == "audio": 
        send_message("audioが送信されました")
        audio_main(message_data['message']['id'])
    else:
        send_message("サポートされていないフォーマットです")
    
    return "hello"


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

if __name__ == "__main__":
    # gunicornで起動する場合
    # gunicorn app:app --bind 0.0.0.0:8080 --workers 4
    app.run(debug=False, port=8080)
