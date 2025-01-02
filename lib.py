import json
import os
import time
import subprocess
import requests
import vertexai

from dotenv import load_dotenv
from google.cloud import speech
from vertexai.generative_models import GenerativeModel
from linebot.v3.messaging import MessagingApi

from const import MODEL, PROJECT_ID, PROMPT, URL

load_dotenv()

line_bot_api = MessagingApi(os.getenv('LINE_API_KEY'))
input_file_name = "temp.m4a"
output_file_name = "output.wav"

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

    PUSH_URL = "https://api.line.me/v2/bot/message/push"
    requests.request("POST", PUSH_URL, headers=headers, data=payload)
    return 'OK'

def write_contents(message_id: str):
    line_api_key = os.getenv('LINE_API_KEY')   
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {line_api_key}'
    }
    CONTENTS_URL = f"https://api-data.line.me/v2/bot/message/{message_id}/content"
    sleep = 1

    for i in range(5):
        time.sleep(sleep)
        contents = requests.get(CONTENTS_URL, headers=headers, stream=True)
        if contents.status_code == 200:
            with open(input_file_name, "wb") as f:
                for chunk in contents.iter_content(chunk_size=1024):
                    if chunk:  # filter out keep-alive new chunks
                        f.write(chunk)
            return
        elif contents.status_code == 202:
            print(f"リトライ: message_id = {message_id}, retry = {i+1}")
            sleep += sleep
        else:
            return f"コンテンツ取得に失敗しました status_code = {contents.status_code}"
    
    return "コンテンツ取得のリトライ処理に失敗しました"

def transcribe_by_speech_to_text(audio_file: str) -> str:
    client = speech.SpeechClient()

    with open(audio_file, "rb") as f:
        audio_content = f.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    speech_script = "";
    for result in response.results:
        speech_script += result.alternatives[0].transcript
    
    return speech_script


def enhance_text_with_gemini(speech_script: str):
    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = GenerativeModel(MODEL)
    prompt = f"{PROMPT} 文章: {speech_script}"
    response = model.generate_content(prompt)
    return response.text

input_file_name = "temp.m4a"
output_file_name = "output.wav"

def convert_to_wav():
    command = f"ffmpeg -i {input_file_name} -ac 1 -ar 16000 -f wav -acodec pcm_s16le -y {output_file_name}"
    subprocess.call(command, shell=True)
