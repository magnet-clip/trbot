from telegram import Bot, Update
from decorators import log_method


@log_method
def start(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text="User")


@log_method
def process(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text="Yo user")


