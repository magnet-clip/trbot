from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, Filters, MessageHandler

GetUrl, AddComments, ChooseChats, PublishOrCancel = range(4)


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

    bot.send_message(chat_id=update.message.chat_id, text="Тут можно ввести комментарий, который будет показан при публикации")
    return AddComments


def publish_comments(bot: Bot, update: Update, user_data):
    user_data['comment'] = update.message.text

    chats = list(map(lambda x: [x], config.get_channel_names()))
    chats.append(["Cancel"])
    markup = ReplyKeyboardMarkup(chats, one_time_keyboard=True)
    bot.send_message(chat_id=update.message.chat_id, text="В какой чат отправить?", reply_markup=markup)

    return ChooseChats


def get_text(user_data):
    if 'comment' in user_data and user_data['comment'] != "":
        return user_data['comment'] + "\r\n" + user_data['article_url']
    else:
        return user_data['article_url']


def publish_chats(bot: Bot, update: Update, user_data):
    channel = update.message.text
    user_data['channel_name'] = channel
    if channel not in config.get_channel_names():
        bot.send_message(chat_id=update.message.chat_id, text="Публикация отменена!")
        return ConversationHandler.END
    else:
        options = [["Yes"], ["No"]]
        bot.send_message(chat_id=update.message.chat_id, text="Подтвердите действие. Отправить статью")
        bot.send_message(chat_id=update.message.chat_id, text=get_text(user_data))
        bot.send_message(chat_id=update.message.chat_id, text="в чат {}?".format(channel),
                         reply_markup=ReplyKeyboardMarkup(options, one_time_keyboard=True))
        return PublishOrCancel


def publish_final(bot: Bot, update: Update, user_data):
    if update.message.text == "Yes":
        bot.send_message(chat_id=config.get_channel_id(user_data['channel_name']), text=get_text(user_data))
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
                AddComments: [MessageHandler(callback=publish_comments, pass_user_data=True, filters=Filters.text)],
                ChooseChats: [MessageHandler(callback=publish_chats, pass_user_data=True, filters=Filters.text)],
                PublishOrCancel: [MessageHandler(filters=Filters.text, callback=publish_final, pass_user_data=True)],
            },
            fallbacks=[CommandHandler("cancel", callback=publish_cancel)]
        )
    ]
