#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages
# This program is dedicated to the public domain under the CC0 license.
import datetime
import logging
from uuid import uuid4

import yaml
from telegram import InlineQueryResultArticle
from telegram import InputTextMessageContent
from telegram.ext import InlineQueryHandler
from telegram.ext import Updater, CommandHandler

import config
import generate

subscriptions = dict()

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

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
    if chat_id in subscriptions:
        update.message.reply_text('You are already subscribed')
        return

    job = job_queue.run_daily(subscribe_notification,
                              context=chat_id,
                              time=datetime.datetime.now().replace(minute=0, hour=8, second=0)
                                   + datetime.timedelta(days=1))
    subscriptions[chat_id] = job
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
        if count > 50:
            update.message.reply_text(str(count) + ' > 50')
            return
        for _ in range(count):
            descriptions.append("+++ " + generate.get_description() + " +++")
        update.message.reply_text("\n".join(descriptions))
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /multiple <count>')


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"' % (update, error))


def inlinequery(bot, update):
    if update.inline_query.query == "":
        count = 3
    else:
        count = int(update.inline_query.query)
    results = list()
    if count > 50:
        count = 50
    for i in range(count):
        description = generate.get_description()
        results.append(InlineQueryResultArticle(id=uuid4(),
                                                title=description,
                                                input_message_content=InputTextMessageContent(description)))
    update.inline_query.answer(results)


def startup(job_queue):
    with open("save.yaml") as json_file:
        save = yaml.load(json_file)
    for s in save["subscriptions"]:
        job = job_queue.run_daily(subscribe_notification, context=s,
                                  time=datetime.datetime.now().replace(minute=0, hour=8, second=0)
                                       + datetime.timedelta(days=1))
        subscriptions[s] = job


def shutdown(a=None, b=None):
    print("------------------------------------------------------------------------")  #
    save = {
        "subscriptions": []
    }
    print(subscriptions)
    for s in subscriptions:
        save["subscriptions"].append(s)
    with open("save.yaml", 'w') as stream:
        yaml.dump(save, stream, default_flow_style=False)


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

    dp.add_handler(CommandHandler("save", shutdown))

    # on noncommand i.e message - echo the message on Telegram
    # dp.add_handler(MessageHandler(Filters.text, single))

    dp.add_handler(InlineQueryHandler(inlinequery))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    startup(updater.job_queue)

    # Run the bot until the you presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

    shutdown()


if __name__ == '__main__':
    main()
