from telegram import Bot, Update, TelegramError
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from config import Config
from database import Database


from actors import user, admin, watcher

import logging

# read config
from helpers.trkd import TRKD

config = Config('config.ini', 'channels.json')
database = Database(config)

# set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARN)
logger = logging.getLogger(__name__)

# set up bot
up = Updater(token=config.telegram_api_key(), workers=32)
dispatcher = up.dispatcher

# save some data
user.config = config
#schedule_manager = ScheduleManager(config)

def error(bot: Bot, update: Update, error: TelegramError):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


if __name__ == "__main__":
    logger.info("Logging into TRKD")
    trkd = TRKD(*config.get_trkd_credentials())
    if not trkd.login():
        logger.error("Failed to login into TRKD")
        exit(-1)

    admins = config.get_admins()

    # Add handlers to dispatcher
    adminFilter = Filters.user(admins)
    notAdminFilter = ~adminFilter

    # Watching users
    for handler in watcher.create_handlers():
        dispatcher.add_handler(handler)

    # Interaction with Admin
    for handler in admin.create_handlers(config, trkd, adminFilter):
        dispatcher.add_handler(handler)

    # for job in schedule_manager.create_jobs():
    #     def execute_and_autoreset(bot, job):
    #         job.callback(bot, job)
    #         up.job_queue.run_once(execute_and_autoreset, job.periodicity)
    #     up.job_queue.run_once(execute_and_autoreset, job.timeout)

    # Interaction with Userд
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
