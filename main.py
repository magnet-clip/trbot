from telegram import Bot, Update
from telegram.error import TelegramError
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from decorators import log_member, log_method
from config import Config

import logging

from enum import Enum

# read config
config = Config('config.ini')

# set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# set up bot
up = Updater(token=config.telegram_api_key(), workers=32)
dispatcher = up.dispatcher


class AdminManager:
    @log_member
    def start(self, bot, update):
        bot.send_message(chat_id=update.message.chat_id, text="Admin")

    @log_member
    def publish_request(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="Publish")
        bot.send_message(config.channels[config.METALS], "Mitol")

    @log_member
    def received_contact(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="Contact")

    @log_member
    def process(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="Yo admin")


class UserManager:
    @log_member
    def start(self, bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="User")

    @log_member
    def process(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="Yo user")


def error(bot: Bot, update: Update, error: TelegramError):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


admin = AdminManager()
user = UserManager()
admins = config.get_admins()


class PublishingStates(Enum):
    Requesting = 1,
    GettingUrl = 2,
    ChoosingChannels = 3,
    Confirming = 4


if __name__ == "__main__":
    # Add handlers to dispatcher
    adminFilter = Filters.user(admins)

    # publishingProcess = {
    #     PublishingStates.Requesting: admin.publisher.request,
    #     PublishingStates.GettingUrl: admin.publisher.getUrl,
    #     PublishingStates.ChoosingChannels: admin.publisher.chooseChannels,
    #     PublishingStates.Confirming: admin.publisher.confirm
    # }
    # dispatcher.add_handler(ConversationHandler(entry_points=[publishHandler], states=publishingProcess, fallbacks=None))

    # Interaction with Admin
    dispatcher.add_handler(CommandHandler(command="start", callback=admin.start, filters=adminFilter))
    publishHandler = CommandHandler(command="publish", callback=admin.publish_request, filters=adminFilter)
    dispatcher.add_handler(publishHandler)
    dispatcher.add_handler(MessageHandler(Filters.text & adminFilter, admin.process))
    dispatcher.add_handler(MessageHandler(Filters.contact & adminFilter, admin.received_contact))

    # Interaction with User
    dispatcher.add_handler(CommandHandler(command="start", callback=user.start, filters=~adminFilter))
    dispatcher.add_handler(MessageHandler(Filters.text & ~adminFilter, user.process))

    # Error handling
    dispatcher.add_error_handler(error)

    # Running the bot
    print("Polling...")
    up.start_polling()
    up.idle()

# class UserHandler:
#     def __init__(self, bot):
#         self.bot = bot
#
#     def landing_page(self):
#         kbd = types.InlineKeyboardMarkup()
#         pass
#
#
# class AdminHandler:
#     def __init__(self, bot):
#         self.bot = bot
#
#     def start_page(self, user_info, env):
#         kbd = types.InlineKeyboardMarkup()
#         kbd.row(types.InlineKeyboardButton("Опубликовать статью", callback_data="/publish_article"))
#         kbd.row(types.InlineKeyboardButton("Список пользователей", callback_data="/show_users"))
#         self.bot.send_message(env.chat_id, "Выберите команду", reply_markup=kbd)


# def validate_access(fun):
#     def validated(*args):
#         message = args[0]
#         user = message.from_user
#         user_info = User(user.first_name, user.last_name, user.id)
#         env = Env(message.text, message.chat.id)
#         if validator.validate_access(message.from_user.id):
#             #theBot.send_message(env.chat_id, "Allowed")
#             return fun(user_info, env)
#         #else:
#             #theBot.send_message(env.chat_id, "Not allowed")
#     return validated
#
#
# def admin_only(fun):
#     def validated(*args):
#         message = args[0]
#         user = message.from_user
#         user_info = User(user.first_name, user.last_name, user.id)
#         env = Env(message.text, message.chat.id)
#         if validator.get_type(message.from_user.id) == UserState.Admin:
#             return fun(user_info, env)
#     return validated


# userHandler = UserHandler(tb)
# adminHandler = AdminHandler(tb)


# @theBot.message_handler(regexp="")

# @theBot.message_handler(commands=['sendmsg'])
# @validate_access
# def handle_send_msg(user_info, env):
#     theBot.send_message(config.channels[config.METALS], "Mitol")
#
#
# @theBot.message_handler(commands=['start', 'help', 'home'])
# @validate_access
# def handle_start_help(user_info, env):
#     print("User %s with id %s said %s" % (user_info.first_name, user_info.user_id, env.text))
#     theBot.send_message(env.chat_id, "SHH")
#     if validator.get_type(user_info.user_id) == access.UserState.Admin:
#         userHandler.landing_page()
#     else:
#         adminHandler.start_page()
#
#
# @theBot.message_handler(func=lambda message: True)
# @validate_access
# def handle_plain_message(user_info, env):
#     print("User %s with id %s said %s" % (user_info.first_name, user_info.user_id, env.text))
#     theBot.send_message(env.chat_id, "Msg [{}]".format(env.text))

# from collections import namedtuple
# User = namedtuple('User', ['first_name', 'last_name', 'user_id'])
# Env = namedtuple('Env', ['text', 'chat_id'])
