import datetime
import threading
from ChatGPT_HKBU import HKBU_ChatGPT
from telegram import Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          CallbackContext)
import configparser
import logging
import mongodb
import os
from Google_Route import Route
from flask import Flask
from probes import startup_probe, readiness_probe, liveness_probe

app = Flask(__name__)
app.add_url_rule('/startup', 'startup', startup_probe)
app.add_url_rule('/readiness', 'readiness', readiness_probe)
app.add_url_rule('/liveness', 'liveness', liveness_probe)


def run_flask_app():
    app.run(port=443)
import yelp



def main():

    # Handle http probes, which are required by Microsoft container app
    # app.run(port=443)
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
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
    dispatcher.add_handler(CommandHandler('yelp',yelp_in_bot))

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
        # Extract the start address and end address from the text entered by the user
        start_add, end_add = extract_addresses_from_context(context.args)
        Start_Address, End_Address, Distance, Duration, Step = google_route.query_route(
            start_add, end_add)      # Get route information
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
                    update.message.reply_text(
                        '   Step' + str(i) + '-' + step["description"])
                elif "Bus Information" in step:
                    subway_info = step["Bus Information"]
                    update.message.reply_text("Bus informarion:\n")
                    for key, value in subway_info.items():
                        update.message.reply_text(key + ": " + str(value))
                    i -= 1
                elif "Subway Information" in step:
                    subway_info = step["Subway Information"]
                    update.message.reply_text("Subway informarion:\n")
                    for key, value in subway_info.items():
                        update.message.reply_text(key + ": " + str(value))
                    i -= 1

    except (IndexError, ValueError):
        update.message.reply_text(
            'Usage: /route S: <start address> E: <end address>')

def yelp_in_bot(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /yelp is issued.

    Args:
        update (Update): This update is a message update.
        context (CallbackContext): The context of the bot's conversation with the user.

    Returns:
        None
    """
    # Extract the location and type parameters from the user's message
    text = update.message.text
    try:
        logging.info(context.args) 
        # Assuming the user's input format is "/yelp location: <location>, type: <type>"
        parts = text.split(' ')
        location_parameter = None
        type_parameter = None
        for part in parts:
            if part.startswith('location:'):
                location_parameter = part.split(':')[1].lstrip()
            elif part.startswith('type:'):
                type_parameter = part.split(':')[1].lstrip()
                #Scan through elements in parts, check if starts with 'location:' or 'type:', and assign the value to location_parameter or type_parameter accordingly.
        if location_parameter is None or type_parameter is None:
            update.message.reply_text('Please provide both location and type parameters in the format: /yelp location: <location>, type: <type>')
            return

        # Use the yelp module to search for businesses based on the location and type parameters
        response = yelp.search(api_key='KJw1YCF5WJzMMwV458YOCd3KRTMhUHjC7SZ5tv24vHKVBWZsDFlm3z9DVyRvtA6_0xMTwnDRUBqPq9od8JVBEp3363UFnvgtKLC0D4pD-FcSuLWvrQvaPgTwcZj4ZXYx',
                                term=type_parameter, location=location_parameter)
        businesses = response.get('businesses')

        if not businesses:
            update.message.reply_text('No businesses found for the given location and type.')
            return

        # Format the response to display the top 5 businesses or the total number of businesses found
        message = 'Businesses found for "{}" in "{}":\n'.format(type_parameter, location_parameter)
        for i, business in enumerate(businesses[:5], start=1):
            message += '{}. {} - {} stars ({} reviews)\n'.format(i, business['name'], business['rating'], business['review_count'])
            message += 'Address: {}\n'.format(', '.join(business['location']['display_address']))
            message += 'Phone Num: {}\n'.format(business['phone'])
        message += '...\n'

        update.message.reply_text(message)
    except Exception as e:
        update.message.reply_text('An error occurred while searching for businesses: {}, Usage: /location: <location>, type: <type>'.format(str(e)))
      

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

    # Fault-tolerance for addresses in case the user does not add a space after "S:" or "E:" when typing.
    for item in address_list:
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
