import vertexai
from google.cloud import speech
from vertexai.generative_models import GenerativeModel

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

    speech_script = "";
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        print(f"Transcript: {result.alternatives[0].transcript}")
        speech_script += result.alternatives[0].transcript
    
    return speech_script


def enhance_text_with_gemini(speech_script: str):
    vertexai.init(project=PROJECT_ID, location="us-central1")
    model = GenerativeModel("gemini-1.5-flash-002")
    prompt = f"この英語の文章の文法の誤りや単語の使い方の指摘を含めて添削をして欲しいです。\
    添削した後の文章と、どの部分をどう修正したのかを教えてください。日本語で修正内容は出して欲しいです。\
    この文章はSpeech to TextでText化したものなので、余計な単語(well, uh)が入っていることがあります。\
    文章: {speech_script}"
    response = model.generate_content(prompt)
    return response.text


def send_message_to_line(gemini_text: str):
    return

  
def main():
    ### 音声を文字にする
    # filepath = '/Users/torinamiko/MyProject/english-app/output.wav'
    # transcribe_by_speech_to_text(filepath)

    ### GeminiAIでtextを添削する
    # sample_text = "today's episode is good way to study uh people has good at what kind of memorize uh you are good at to remember uh I believe I'm good uh to visualize memo memorize visual visualize way to memorize something I when I was student I take a note with some elastic withdrawing some illustration and then take a note so I'm good at to visualize memorization I hope this uh study way to improve my this way to help my study my study effectively"
    # gemini_response = enhance_text_with_gemini(sample_text)
    # print(gemini_response)

    ### LINEに添削したTextを送る
    gemini_sample_res = '''
元の文章：today's episode is good way to study uh people has good at what kind of memorize uh you are good at to remember uh I believe I'm good uh to visualize memo memorize visual visualize way to memorize something I when I was student I take a note with some elastic withdrawing some illustration and then take a note so I'm good at to visualize memorization I hope this uh study way to improve my this way to help my study my study effectively


添削後：Today's episode is a good way to study how people effectively memorize information.  I believe I'm good at visualizing, and I use this method to memorize. When I was a student, I would take notes, incorporating illustrations and diagrams to aid recall.  Therefore, I excel at visual memorization. I hope this study method will improve my academic performance.


修正内容：

1. **"is good way" → "is a good way"**:  冠詞「a」を追加して文法的に正しい表現にしました。

2. **"to study uh people has good at what kind of memorize" → "to study how people effectively memorize information"**:  曖昧で非文法的な部分を、より明確で自然な表現に書き換えました。「how people effectively memorize information」で、人がどのように効果的に記憶するかを主題にしています。

3. **"you are good at to remember"**: この部分は削除しました。文脈上、不必要で、流れを妨げていました。

4. **"I believe I'm good uh to visualize memo memorize visual visualize" → "I believe I'm good at visualizing, and I use this method to memorize."**:  繰り返しが多く、曖昧な表現を簡潔で分かりやすい表現に修正しました。「memo」と「visual」の重複を解消し、「visualizing」という動名詞を用いることで自然な表現にしました。

5. **"way to memorize something I when I was student I take a note" → "When I was a student, I would take notes,"**:  接続詞と時制の一貫性を保つように修正しました。「I would take notes」を使うことで、過去の習慣的な行動を表しています。

6. **"with some elastic withdrawing some illustration and then take a note" → "incorporating illustrations and diagrams to aid recall."**:  「elastic」の意味が不明瞭で、「withdrawing」も文脈に合わないため、より自然で分かりやすい表現に書き換えました。「incorporating illustrations and diagrams to aid recall」は、イラストや図表を組み込むことで記憶を助けることを意味します。

7. **"so I'm good at to visualize memorization" → "Therefore, I excel at visual memorization."**:  「to visualize memorization」をより自然な「visual memorization」に変更し、「so I'm good at」をよりフォーマルな「Therefore, I excel at」に置き換えました。

8. **"I hope this uh study way to improve my this way to help my study my study effectively" → "I hope this study method will improve my academic performance."**:  冗長で曖昧な表現を簡潔で効果的な表現に修正しました。「academic performance」は学業成績を意味し、文脈に合致しています。  重複していた「my study」も削除しました。


全体的に、元の文章はSpeech to Text特有の断片的な表現や、文法的な誤りが多く含まれていました。添削後の文章は、より流暢で、内容も明確に伝わります。
'''

main()
