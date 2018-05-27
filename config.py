import os
from celery.schedules import crontab

broker_url = os.getenv('BROKER_URL','pyamqp://guest@localhost//')
result_backend = os.getenv('CELERY_RESULT_BACKEND','db+sqlite:///celery-results.sqlite')

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'America/Sao_Paulo'
enable_utc = True

beat_schedule = {
    'telegram_polling': {
        'task': 'tasks.telegram_polling',
        'schedule': 5.0,
        # 'args': (16, 16),
    },
    # Calls test('world') every 30 seconds
    # 'test': {
    #     'task': 'tasks.first_task.add',
    #     'schedule': 30.0,
    #     'args': (16, 16),
    # },
    # Executes every Monday morning at 7:30 a.m.
    # 'add-every-monday-morning': {
    #     'task': 'tasks.first_task.hello',
    #     'schedule': crontab(hour=7, minute=30, day_of_week=1),
    #     'args': 'Boa segunda-feira!',
    # },
}

telegram = {
    'token': os.getenv('TELEGRAM_BOT_TOKEN', None),
}

budget_spreadsheet = os.getenv('SPREADSHEET')