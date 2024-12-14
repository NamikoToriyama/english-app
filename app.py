import json
import os

import requests
import vertexai
from dotenv import load_dotenv
from google.cloud import speech
from vertexai.generative_models import GenerativeModel

from const import MODEL, PROJECT_ID, PROMPT, URL

# .envファイルを読み込む
load_dotenv()

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


def send_message_to_line(gemini_text: str):
    line_api_key = os.getenv('LINE_API_KEY')
    user_id = os.getenv('LINE_MY_USER_ID')

    payload = json.dumps({
    "to": user_id,
    "messages": [
        {
        "type": "text",
        "text": gemini_text
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {line_api_key}'
    }

    response = requests.request("POST", URL, headers=headers, data=payload)
    print(response.status_code)
    return response.status_code

  
def main():
    ### 音声を文字にする
    filepath = '/Users/torinamiko/MyProject/english-app/output.wav'
    speech_script = transcribe_by_speech_to_text(filepath)

    ### GeminiAIでtextを添削する
    gemini_response = enhance_text_with_gemini(speech_script)
    print(gemini_response)

    ### LINEに添削したTextを送る
    status_code = send_message_to_line(gemini_response)
    if status_code != 200:
        print("Error happens")

main()

