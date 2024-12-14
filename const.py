PROJECT_ID="torichan-english-study-tori"
PROMPT="""この英語の文章の文法の誤りや単語の使い方の指摘を含めて添削をして欲しいです。
    添削した後の文章と、どの部分をどう修正したのかを教えてください。日本語で修正内容は出して欲しいです。
    この文章はSpeech to TextでText化したものなので、余計な単語(well, uh)が入っていることがあります。"""
URL = "https://api.line.me/v2/bot/message/push"
MODEL="gemini-1.5-flash-002"
