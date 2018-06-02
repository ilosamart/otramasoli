import os

telegram = {
    'token': os.getenv('TELEGRAM_BOT_TOKEN', None),
}

budget_spreadsheet = os.getenv('SPREADSHEET')