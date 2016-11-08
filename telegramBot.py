#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import config
import generate

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def help(bot, update):
    update.message.reply_text("Hier steht der Hilfetext!")


def echo(bot, update):
    update.message.reply_text(update.message.text)


def multiple(bot, update, args):
    try:
        descriptions = []
        print(args)
        count = int(args[0])
        if count > 100:
            update.message.reply_text(str(count) + ' > 100')
            return
        for _ in range(count):
            descriptions.append("+++ " + generate.get_description() + " +++")
        update.message.reply_text("\n".join(descriptions))
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /multiple <count>')


def error(bot, update, error):
    logger.warn('Update "%s" caused error "%s"' % (update, error))


def main():
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(config.telegram_bot_token)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", help))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("multiple", multiple, pass_args=True))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
