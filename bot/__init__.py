import time
from datetime import date

import telepot
from telepot.routing import (by_content_type, make_content_type_routing_table,
                             lower_key, by_chat_command, make_routing_table,by_regex)

from config import telegram
from googlespreadsheet import *


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
        nubank = 'nubank'
        visa = 'visa'
        beleza = 'beleza'

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

    def _registra_despesa(self, valor=0.0, tipo=None, data=date.today(), autor=''):
        gc = gspread.authorize(credentials)

        sps = gc.open_by_url(budget_spreadsheet)

        # sps.add_worksheet('2018-05', 1, 3)

        # sps.add_worksheet('2018-06', 1, 3)

        wks = sps.worksheet('2018-06')
        wks.append_row([data.strftime('%Y-%m'), tipo, valor, autor])

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
        self._registra_despesa(valor=self._remove_command_from_message(msg),
                               tipo=CommandHandler.TipoDespesa.refeicao,
                               autor=msg['from']['first_name'])

    def on_lazer(self, msg):
        self._registra_despesa(valor=self._remove_command_from_message(msg),
                               tipo=CommandHandler.TipoDespesa.lazer,
                               autor=msg['from']['first_name'])

    def on_luiz(self, msg):
        self._registra_despesa(valor=self._remove_command_from_message(msg),
                               tipo=CommandHandler.TipoDespesa.luiz,
                               autor=msg['from']['first_name'])

    def on_aluguel(self, msg):
        self._registra_despesa(valor=self._remove_command_from_message(msg),
                               tipo=CommandHandler.TipoDespesa.aluguel,
                               autor=msg['from']['first_name'])

    def on_net(self, msg):
        self._registra_despesa(valor=self._remove_command_from_message(msg),
                               tipo=CommandHandler.TipoDespesa.net,
                               autor=msg['from']['first_name'])

    def on_outro(self, msg):
        self._registra_despesa(valor=self._remove_command_from_message(msg),
                               tipo=CommandHandler.TipoDespesa.outro,
                               autor=msg['from']['first_name'])

    def on_nubank(self, msg):
        self._registra_despesa(valor=self._remove_command_from_message(msg),
                               tipo=CommandHandler.TipoDespesa.nubank,
                               autor=msg['from']['first_name'])

    def on_visa(self, msg):
        self._registra_despesa(valor=self._remove_command_from_message(msg),
                               tipo=CommandHandler.TipoDespesa.visa,
                               autor=msg['from']['first_name'])

    def on_beleza(self, msg):
        self._registra_despesa(valor=self._remove_command_from_message(msg),
                               tipo=CommandHandler.TipoDespesa.beleza,
                               autor=msg['from']['first_name'])


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
                       'nubank',
                       'visa',
                       ((None,), self.command_handler.on_invalid_text),
                       (None, self.command_handler.on_invalid_command),
                   ])
                   )


bot = MeuBot(telegram['token'])