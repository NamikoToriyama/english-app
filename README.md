# English-APP

## Start Environment
```
python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt
```

## Output Requirement
```
pip freeze > requirements.txt
 ```

## Run Local
```
export GOOGLE_APPLICATION_CREDENTIALS="torichan-english-study-tori-9f676c330598.json"
python app.py
```

## How to create sample file
```
ffmpeg -i sample.m4a -ac 1 -ar 16000 -f wav -acodec pcm_s16le output.wav
```
