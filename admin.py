from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, Filters, MessageHandler

from config import Config

GetUrl, ChooseChats, PublishOrCancel = range(3)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Admin")


def received_contact(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text="Contact")


def process(bot: Bot, update: Update):
    bot.send_message(chat_id=update.message.chat_id, text="Yo admin")


def publish_request(bot: Bot, update: Update):
    """Fist step for publishing"""
    bot.send_message(chat_id=update.message.chat_id, text="Скопируйте сюда сслылку на статью для публикации")
    return GetUrl


def publish_url(bot: Bot, update: Update, user_data):
    global config

    # todo check if url is correct
    user_data['article_url'] = update.message.text
    chats = list(map(lambda x: [x], config.get_channel_names()))
    chats.append(["Cancel"])
    markup = ReplyKeyboardMarkup(chats, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="В какой чат отправить?", reply_markup=markup)
    return ChooseChats


def publish_chats(bot: Bot, update: Update, user_data):
    channel = update.message.text
    user_data['channel_name'] = channel
    if channel not in config.get_channel_names():
        bot.send_message(chat_id=update.message.chat_id, text="Публикация отменена!")
        return ConversationHandler.END
    else:
        options = [["Yes"], ["No"]]
        bot.send_message(chat_id=update.message.chat_id, text="Отправить статью")
        bot.send_message(chat_id=update.message.chat_id, text=user_data['article_url'])
        bot.send_message(chat_id=update.message.chat_id, text="В чат {}?".format(channel),
                         reply_markup=ReplyKeyboardMarkup(options, one_time_keyboard=True))
        return PublishOrCancel


def publish_final(bot: Bot, update: Update, user_data):
    if update.message.text == "Yes":
        bot.send_message(chat_id=config.get_channel_id(user_data['channel_name']), text=user_data['article_url'])
        bot.send_message(chat_id=update.message.chat_id, text="Published successfully")
    else:
        bot.send_message(chat_id=update.message.chat_id, text="Publishing cancelled")
    return ConversationHandler.END


def publish_cancel(bot: Bot, update: Update, user_data):
    bot.send_message(chat_id=update.message.chat_id, text="Won't publish")
    return ConversationHandler.END


def create_handlers(admin_filter):
    return [
        # - Start command
        CommandHandler(command="start", callback=start, filters=admin_filter),

        # - Incoming contact details
        ConversationHandler(
            entry_points=[CommandHandler(command="publish", callback=publish_request, filters=admin_filter)],
            states={
                GetUrl: [MessageHandler(filters=Filters.text, callback=publish_url, pass_user_data=True)],
                ChooseChats: [MessageHandler(callback=publish_chats, pass_user_data=True, filters=Filters.text)],
                PublishOrCancel: [MessageHandler(filters=Filters.text, callback=publish_final, pass_user_data=True)],
            },
            fallbacks=[CommandHandler("cancel", callback=publish_cancel)]
        )
    ]
