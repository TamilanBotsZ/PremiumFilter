FROM python:3.8

WORKDIR /VoiceOfSha

COPY requirements.txt ./

RUN pip install -r requirements.txt

CMD ["python3", "bot.py"]
