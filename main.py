from telegram import Bot, Update, TelegramError
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import Config
from database import Database

from actors import user, admin, watcher

import logging

# read config
config = Config('config.ini')
database = Database(config)

# set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# set up bot
up = Updater(token=config.telegram_api_key(), workers=32)
dispatcher = up.dispatcher

# save some data
user.config = config


def error(bot: Bot, update: Update, error: TelegramError):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == "__main__":
    admins = config.get_admins()

    # Add handlers to dispatcher
    adminFilter = Filters.user(admins)
    notAdminFilter = ~adminFilter

    # Watching users
    for handler in watcher.create_handlers():
        dispatcher.add_handler(handler)

    # Interaction with Admin
    for handler in admin.create_handlers(config, adminFilter):
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
