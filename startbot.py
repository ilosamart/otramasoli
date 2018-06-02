from telepot.loop import MessageLoop

from bot import bot


def handle(msg):
    print(msg)
    bot.on_message(msg)


MessageLoop(bot, handle=handle).run_forever(relax=5)
