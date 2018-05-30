import os
from datetime import datetime, timedelta
import time

from celery import Celery

from bot import bot

CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND','file:///tmp/')
BROKER_URL = os.getenv('BROKER_URL','pyamqp://guest@localhost//')

app = Celery('tasks')
app.config_from_object('config')


@app.task(bind=True)
def telegram_polling(self):
    try:
        response = bot.getUpdates(offset=self.last_update_id+1)
    except:
        response = bot.getUpdates()
    # [{'message': {'chat': {'first_name': 'Nick',
    #                        'id': 999999999,
    #                        'type': 'private'},
    #               'date': 1465283242,
    #               'from': {'first_name': 'Nick', 'id': 999999999},
    #               'message_id': 10772,
    #               'text': 'Hello'},
    #   'update_id': 100000000}]
    for message in response:
        # reply_message.delay(message['message']['chat']['id'], message['message']['text'])
        bot.on_message(message['message'])
        self.last_update_id = message['update_id']
    return 'OK'


@app.task(bind=True)
def reply_message(self, chat_id, message):
    try:
        bot.sendChatAction(chat_id, "typing")
        time.sleep(0.5)
        bot.sendMessage(chat_id, u"That was she said:" + message)
    except Exception as err:
        self.retry(exc=err, max_retries=3, eta=datetime.now()+timedelta(minutes=1))
    return 'OK'