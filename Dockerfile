FROM python:3

RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

COPY . .

RUN python3 -m pip install -r requirements.txt

CMD ["python3", "bot.py"]