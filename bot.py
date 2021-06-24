# -*- coding: utf-8 -*-
"""bot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1R8edSLzj6p1BZKir1t7u8hgrwOMcW-zs
"""

import logging
import os

import telegram
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import tensorflow
from tensorflow.keras import models


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, context: CallbackContext) -> None:
  update.message.reply_text('Hi send an image to classify!')


def help_command(update: Update, context: CallbackContext) -> None:
  update.message.reply_text('Help!')


def load_model():
  print('Teleg version: ', telegram.__version__)
  global model
  model = models.load_model('model.h5')
  print('Model Loaded')

def photo(update: Update, context: CallbackContext) -> int:
  user = update.message.from_user
  photo_file = update.message.photo[-1].get_file()
  photo_file.download('user_photo.jpg')
  print(type(photo_file))
  logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
#   img = tensorflow.image.resize(photo_file, (
  label = model.predict('user_photo.jpg')
  print('Label: ', label)
  if label > 0.5:
    update.message.reply_text('Damage Detected!!!')
  else:
    update.message.reply_text('No Damage Detected...')
  update.message.reply_text('I m working!')


def main():
  # Create the Updater and pass it your bot's token.
  load_model()
  TOKEN = "1847936147:AAF9wmalqDW87DgwioOQbOqgIiwS4z4V67s" # place your token here
  updater = Updater(TOKEN, use_context=True)
  PORT = int(os.environ.get('PORT', '8443'))

  # Get the dispatcher to register handlers
  dispatcher = updater.dispatcher

  # on different commands - answer in Telegram
  dispatcher.add_handler(CommandHandler("start", start))
  dispatcher.add_handler(CommandHandler("help", help_command))
  dispatcher.add_error_handler(CallbackContext)
  # on noncommand i.e message - echo the message on Telegram
  dispatcher.add_handler(MessageHandler(Filters.photo, photo)) 

  updater.start_webhook(listen="0.0.0.0",  port=PORT, url_path=TOKEN, webhook_url="https://tipregofunziona.herokuapp.com/" + TOKEN)
  # updater.bot.set_webhook("https://telegbottry.herokuapp.com/" + TOKEN)
  updater.start_polling()
  updater.idle()

if __name__ == '__main__':
  main()
