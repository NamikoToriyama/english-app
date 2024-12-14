# this is for cloud function
from google.cloud import speech

PROJECT_ID="torichan-english-study-tori"

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

    text = "";
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(f"Transcript: {result.alternatives[0].transcript}")
        text += result.alternatives[0].transcript
    
    return text


# from google.cloud import aiplatform
import vertexai
from vertexai.generative_models import GenerativeModel


def enhance_text_with_gemini(text: str):
    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-002")
    prompt = f"この英語の文章の文法の誤りや単語の使い方の指摘を含めて添削をして欲しいです。\
    添削した後の文章と、どの部分をどう修正したのかを教えてください。\
    この文章はSpeech to TextでText化したものなので、余計な単語(well, uh)が入っていることがあります。\
    文章: {text}"
    response = model.generate_content(prompt)
    return response.text


  
def main():
    ### 音声を文字にする
    # filepath = '/Users/torinamiko/MyProject/english-app/output.wav'
    # transcribe_by_speech_to_text(filepath)

    ### GeminiAIでtextを添削する
    # sample_text = "today's episode is good way to study uh people has good at what kind of memorize uh you are good at to remember uh I believe I'm good uh to visualize memo memorize visual visualize way to memorize something I when I was student I take a note with some elastic withdrawing some illustration and then take a note so I'm good at to visualize memorization I hope this uh study way to improve my this way to help my study my study effectively"
    # gemini_response = enhance_text_with_gemini(sample_text)

    ### LINEに添削したTextを送る
    gemini_sample_res = '''
The original text is quite fragmented and grammatically incorrect due to the nature of speech-to-text transcription.  Here's a corrected version, with explanations of the changes:

**Original Text:** today's episode is good way to study uh people has good at what kind of memorize uh you are good at to remember uh I believe I'm good uh to visualize memo memorize visual visualize way to memorize something I when I was student I take a note with some elastic withdrawing some illustration and then take a note so I'm good at to visualize memorization I hope this uh study way to improve my this way to help my study my study effectively

**Corrected Text:** Today's episode is a good way to study how people effectively memorize information.  I believe my strength lies in visual memorization.  When I was a student, I used to take notes incorporating illustrations and diagrams, which helped me remember things better. I hope this study method will improve my study efficiency.


**Changes Made and Explanations:**

* **"is good way" changed to "is a good way":**  The original phrasing lacked the indefinite article "a."
* **"to study uh people has good at what kind of memorize" changed to "how people effectively memorize information":** This completely restructures the unclear and grammatically incorrect phrase.  It clarifies the topic to be about *how* people memorize, not just that they do.  "effectively" is added for better flow and precision.
* **Removed redundant "uh" instances:** All instances of "uh" were filler words and have been removed for clarity and better writing.
* **"you are good at to remember" removed:** This was redundant as the focus shifts to the speaker's personal memorization method.
* **"I believe I'm good uh to visualize memo memorize visual visualize way to memorize something" changed to "I believe my strength lies in visual memorization":** This significantly improves clarity and conciseness. The repetition of "visualize" and "memorize" has been removed, and the phrasing is made more natural.
* **"I when I was student I take a note with some elastic withdrawing some illustration and then take a note" changed to "When I was a student, I used to take notes incorporating illustrations and diagrams":** This sentence was grammatically incorrect and confusing.  "elastic withdrawing" is unclear; it's assumed this referred to using some kind of flexible binding or drawing materials. The revised version clarifies the method used.  "diagrams" is used instead of "illustration" for broader accuracy.
* **"so I'm good at to visualize memorization" changed to "which helped me remember things better":**  The original phrasing was grammatically incorrect. The revised version improves flow and is more concise.
* **"I hope this uh study way to improve my this way to help my study my study effectively" changed to "I hope this study method will improve my study efficiency":**  This final sentence was extremely wordy and repetitive. The revised version is concise and uses the more precise term "study efficiency."


The corrected text is significantly more grammatically correct, clearer, and more concise than the original.  It reads smoothly and conveys the speaker's intended meaning effectively.
'''

main()
