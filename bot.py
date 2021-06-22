import logging
import os

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
  # calling model func
#import tensorflow
#from tensorflow.keras import models

#rec = models.load_model('T1Res152-FT.h5')
#recognition = [rec]

#def recognition_analysis(target):
#  # save_and_display_gradcam(x_t[n_img], models)
#  pred = 0
#  for i in recognition:
#    pred += i.predict(target)
#  pred = pred / len(recognition)

#  dam = pred[0]
#  dam = round(dam[0]*100, 2)
  
#  return dam



# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi send an image to classify!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def photo(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Okay now wait a few seconds!!!'
    )
    #if recognition != None:
    #    dam = recognition_analysis('user_photo.jpg')
    #    update.message.reply_text(dam)

    update.message.reply_text('I m working!')


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    TOKEN = "1847936147:AAF9wmalqDW87DgwioOQbOqgIiwS4z4V67s" # place your token here
    updater = Updater(TOKEN, use_context=True)
    PORT = int(os.environ.get('PORT', '8443'))

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.photo & ~Filters.command, photo))

    updater.start_webhook(listen="0.0.0.0",
                      port=PORT,
                      url_path=TOKEN,
		      webhook_url="https://telegbottry.herokuapp.com/" + TOKEN)
    # updater.bot.set_webhook("https://telegbottry.herokuapp.com/" + TOKEN)
    updater.idle()

if __name__ == '__main__':
    main()