FROM python:3.11.2
#.          👆👆
#change 3.10 to 3.11.2 if you depolying heroku or koyeb

WORKDIR /TamilanBotsz

COPY requirements.txt ./

RUN pip install -r requirements.txt

copy . .

CMD ["python3", "bot.py"]
