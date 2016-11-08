#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
import re
from uuid import uuid4

from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram import ParseMode
from telegram.ext import InlineQueryHandler
from telegram.ext import Job
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

import config
import generate

subscriptions = dict()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.DEBUG)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.

def help(bot, update):
    update.message.reply_text("Hier steht der Hilfetext!")


def single(bot, update):
    update.message.reply_text(generate.get_description())


def subscribe_notification(bot, job):
    bot.sendMessage(job.context, text=generate.get_description())


def subscribe(bot, update, job_queue):
    """Adds a job to the queue"""
    chat_id = update.message.chat_id
    # Add job to queue
    job = Job(subscribe_notification, 10, repeat=True, context=chat_id)
    subscriptions[chat_id] = job
    job_queue.put(job, next_t=0.0)
    update.message.reply_text('Successfully subscribed')


def unsubscribe(bot, update):
    """Deletes a job"""
    chat_id = update.message.chat_id

    if chat_id not in subscriptions:
        update.message.reply_text('You have no subscription')
        return

    # Add job to queue
    job = subscriptions[chat_id]
    job.schedule_removal()
    del subscriptions[chat_id]
    update.message.reply_text('Successfully unsubscribed')


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
    dp.add_handler(CommandHandler("single", single))
    dp.add_handler(CommandHandler("multiple", multiple, pass_args=True))
    # dp.add_handler(CommandHandler("single", subscribe_notification))
    dp.add_handler(CommandHandler("subscribe", subscribe, pass_job_queue=True))
    dp.add_handler(CommandHandler("unsubscribe", unsubscribe))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, single))

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
