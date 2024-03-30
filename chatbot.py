import datetime
from ChatGPT_HKBU import HKBU_ChatGPT
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)
import configparser
import logging
import mongodb
import os


def main():
    # Load your token and create an Updater for your Bot
    telegram_token = os.environ['BOT_TOKEN']
    updater = Updater(
        token=(telegram_token), use_context=True)
    dispatcher = updater.dispatcher

    # # You can set this logging module, so you will know when
    # # and why things do not work as expected Meanwhile, update your config.ini as:
    # logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #                     level=logging.INFO)
    # # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)
    # on different commands - answer in Telegram

    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~
                                          Filters.command, handle_message))

    # register a dispatcher to handle message: here we register an echo dispatcher
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
    # dispatcher.add_handler(echo_handler)
    # dispatcher for chatgpt

    # global chatgpt
    # chatgpt = HKBU_ChatGPT(config)
    # chatgpt_handler = MessageHandler(Filters.text & (~Filters.command),
    #  equiped_chatgpt)
    # dispatcher.add_handler(chatgpt_handler)

    # To start the bot:
    updater.start_polling()
    updater.idle()


def echo(update, context):
    reply_message = update.message.text.upper()
    logging.info("Update: " + str(update))
    logging.info("context: " + str(context))
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=reply_message)
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text(
        'Do you need some help for your HongKong travel?')


def hello_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /hello is issued."""
    try:
        logging.info(context.args[0])
        msg = context.args[0]  # /add keyword <-- this should store the keyword
        update.message.reply_text('Good day ' + msg + '!')
    except (IndexError, ValueError):
        update.message.reply_text('Good day!')


# def equiped_chatgpt(update, context):
#     global chatgpt
#     reply_message = chatgpt.submit(update.message.text)
#     logging.info("Update: " + str(update))
#     logging.info("context: " + str(context))
#     context.bot.send_message(
#         chat_id=update.effective_chat.id, text=reply_message)

def handle_message(update, context):

    # add your process of bot_reply

    bot_reply = "zsbdddd"
    mongodb.storage(update, context, bot_reply)
    update.message.reply_text(bot_reply)


if __name__ == '__main__':
    main()
