FROM python:3.10

WORKDIR /PremiumFilter

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "bot.py"]
