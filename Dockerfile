FROM python:3.11

WORKDIR /PremiumFilter

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "bot.py"]
