import datetime
from ChatGPT_HKBU import HKBU_ChatGPT
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)
import configparser
import logging
import mongodb
import os
from Google_Route import Route


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

    global google_route
    google_route = Route()
    dispatcher.add_handler(CommandHandler("route", route))

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

def route(update: Update, context: CallbackContext) -> None:
	"""Send a message when the command /route is issued."""
	try:
		global google_route
		i = 0
		logging.info(context.args)          # Get the text entered by the user
		start_add, end_add = extract_addresses_from_context(context.args)           # Extract the start address and end address from the text entered by the user
		Start_Address,End_Address,Distance,Duration,Step = google_route.query_route(start_add,end_add)      # Get route information
		if Start_Address is None:
			update.message.reply_text('Your input maybe wrong, please check')
		else:
			update.message.reply_text('Start Address: ' + Start_Address +
								  	  '\nEnd Address: ' + End_Address +
									  '\nDistance: ' + Distance +
									  '\nDuration: ' + Duration)
			for step in Step:       # Show the user each step in the route, and if there is a step to take the metro or bus, show the information about the metro or bus to be taken.
				i += 1
				if "description" in step:
					update.message.reply_text('   Step'+ str(i) + '-' + step["description"])
				elif "Bus Information" in step:
					subway_info = step["Bus Information"]
					update.message.reply_text("Bus informarion:\n")
					for key, value in subway_info.items():
						update.message.reply_text( key + ": " + str(value))
					i -= 1
				elif "Subway Information" in step:
					subway_info = step["Subway Information"]
					update.message.reply_text("Subway informarion:\n")
					for key, value in subway_info.items():
						update.message.reply_text( key + ": " + str(value))
					i -= 1

	except (IndexError, ValueError):
		update.message.reply_text('Usage: /route S: <start address> E: <end address>')

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

def extract_addresses_from_context(address_list):
    """This function is used to retrieve the start address and end address from the text entered by the user."""
    start = ''
    end = ''
    start_flag = False
    end_flag = False

    for item in address_list:       # Fault-tolerance for addresses in case the user does not add a space after "S:" or "E:" when typing.
        if item.startswith("S:"):
            start += item[len("S:"):].strip() + " "
            start_flag = True
        elif item.startswith("E:"):
            end += item[len("E:"):].strip() + " "
            end_flag = True
            start_flag = False
        elif start_flag:
            start += item + ' '
        elif end_flag:
            end += item + ' '

    return start.strip(), end.strip()

if __name__ == '__main__':
    main()
