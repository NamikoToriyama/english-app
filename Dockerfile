FROM python:3.9

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . .

ENV DEBIAN_FRONTEND=noninteractive
RUN apt update && apt install -y ffmpeg

RUN pip install -r requirements.txt      
CMD gunicorn app:app --bind 0.0.0.0:8080 --workers 4
