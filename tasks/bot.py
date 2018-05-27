import time
from datetime import date

import telepot
from telepot.routing import (by_content_type, make_content_type_routing_table,
                             lower_key, by_chat_command, make_routing_table,by_regex)

from celeryconfig import telegram
from googlespreadsheet.budget import wks


class CommandHandler(object):

    _template_messages = {
        'welcome': 'Bem-vindo ao bot do Fábio!',
        'unrecognized': 'Desculpe, não entendi :/',
    }

    class TipoDespesa:
        refeicao = 'refeicao'
        lazer = 'lazer'
        luiz = 'luiz'
        aluguel = 'aluguel'
        net = 'net'
        outro = 'outro'

    """
    Sample message

    {'chat': {'first_name': 'Nick',
              'id': 999999999,
              'type': 'private'},
     'date': 1465283242,
     'from': {'first_name': 'Nick', 'id': 999999999},
     'message_id': 10772,
     'text': 'Hello'}
    """
    def _reply_with_thinking_time(self, msg, reply, thinking_time=0.5):
        bot.sendChatAction(msg['chat']['id'], "typing")
        time.sleep(thinking_time)
        bot.sendMessage(msg['chat']['id'], reply)

    def _remove_command_from_message(self, msg):
        return ' '.join(msg['text'].split(' ')[1:])

    def _registra_despesa(self, valor=0.0, tipo=None, data=date.today()):
        wks.append_row([data.strftime('%Y-%m'), tipo, valor])

    def on_start(self, msg):
        self._reply_with_thinking_time(msg, self._template_messages['welcome'])

    def on_echo(self, msg):
        text = self._remove_command_from_message(msg)
        self._reply_with_thinking_time(msg, 'ECHO | {}\nSua mensagem original é: {}'.format(text, msg))

    def on_settings(self, msg):
        print('Command: settings', msg)

    def on_invalid_text(self, msg):
        self._reply_with_thinking_time(msg, self._template_messages['unrecognized'])

    def on_invalid_command(self, msg):
        # self._reply_with_thinking_time(msg,self._template_messages['unrecognized'])
        self.on_invalid_text(msg)

    def on_refeicao(self, msg):
        self._registra_despesa(valor=self._remove_command_from_message(msg), tipo=CommandHandler.TipoDespesa.refeicao)

    def on_lazer(self, msg):
        self._registra_despesa(0, CommandHandler.TipoDespesa.lazer)

    def on_luiz(self, msg):
        self._registra_despesa(0, CommandHandler.TipoDespesa.luiz)

    def on_aluguel(self, msg):
        self._registra_despesa(0, CommandHandler.TipoDespesa.aluguel)

    def on_net(self, msg):
        self._registra_despesa(0, CommandHandler.TipoDespesa.net)

    def on_outro(self, msg):
        self._registra_despesa(0, CommandHandler.TipoDespesa.outro)


class MeuBot(telepot.Bot, telepot.helper.DefaultRouterMixin):
    def __init__(self, *args, **kwargs):
        super(MeuBot, self).__init__(*args, **kwargs)
        self.command_handler = CommandHandler()
        self._router = telepot.helper.\
            Router(lower_key(by_chat_command()),
                   make_routing_table(self.command_handler, [
                       'start',
                       'settings',
                       'echo',
                       'refeicao',
                       'lazer',
                       'luiz',
                       'aluguel',
                       'net',
                       'outro',
                       ((None,), self.command_handler.on_invalid_text),
                       (None, self.command_handler.on_invalid_command),
                   ])
                   )


bot = MeuBot(telegram['token'])