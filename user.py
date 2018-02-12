from telegram import Bot, Update


def start(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text="User")


def process(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text="Yo user")


