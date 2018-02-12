from telegram import Bot, Update, TelegramError
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from config import Config

import admin
import user

import logging

# read config
config = Config('config.ini')

# set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# set up bot
up = Updater(token=config.telegram_api_key(), workers=32)
dispatcher = up.dispatcher

# save some data
admin.config = config
user.config = config


def error(bot: Bot, update: Update, error: TelegramError):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == "__main__":
    admins = config.get_admins()

    # Add handlers to dispatcher
    adminFilter = Filters.user(admins)
    notAdminFilter = ~adminFilter

    # Interaction with Admin
    for handler in admin.create_handlers(adminFilter):
        dispatcher.add_handler(handler)

    # Interaction with User
    # # - Start command
    dispatcher.add_handler(CommandHandler(command="start", callback=user.start, filters=notAdminFilter))
    # - Any text message
    dispatcher.add_handler(MessageHandler(Filters.text & notAdminFilter, user.process))

    # Error handling
    dispatcher.add_error_handler(error)

    # Running the bot
    print("Polling...")
    up.start_polling()
    up.idle()
