# OTramasoli

This is a little bot to:
* learn to interact with the TelegramAPI
* learn Celery
* help me organize my expenses

## How it works

Currently this bot is composed of:
* Celery worker and beat scheduler
* Telegram Bot
* Google Spreadsheet

Every five seconds or so the _beat_ scheduler gets new messages from
Telegram (so it uses polling 'cause it's intended to run on a Raspeberry PI
that doesn't have a public API endpoint :smiley:).

For each new message received it triggers a new task to process it.

The bot has a few commands specified, each one is intended to register a
certain kind o expense in the form:
* /expense_type expense_value expense_description, eg:
  * /refeicao 25,50 almoço

## TODO: Configuration

## TODO: More docs