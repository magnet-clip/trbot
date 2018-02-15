from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, Filters, MessageHandler

from config import Config


class Publish:
    GetUrl, AddComments, ChooseChats, PublishOrCancel = range(4)


class Admin:
    def __init__(self, config: Config):
        self.config = config

    def start(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="Admin")

    def received_contact(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="Contact")

    def process(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="Yo admin")

    def publish_request(self, bot: Bot, update: Update):
        """Fist step for publishing"""
        bot.send_message(chat_id=update.message.chat_id, text="Скопируйте сюда сслылку на статью для публикации")
        return Publish.GetUrl

    def publish_url(self, bot: Bot, update: Update, user_data):
        # todo check if url is correct
        user_data['article_url'] = update.message.text

        bot.send_message(chat_id=update.message.chat_id, text="Тут можно ввести комментарий, который будет показан при публикации. Если комментарий не требуется, введите знак -")
        return Publish.AddComments

    def publish_comments(self, bot: Bot, update: Update, user_data):
        user_data['comment'] = update.message.text

        chats = list(map(lambda x: [x], self.config.get_channel_names()))
        chats.append(["Cancel"])
        markup = ReplyKeyboardMarkup(chats, one_time_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text="В какой чат отправить?", reply_markup=markup)

        return Publish.ChooseChats

    def get_text(self, user_data):
        if 'comment' in user_data and user_data['comment'].strip() != "-":
            return user_data['comment'] + "\r\n" + user_data['article_url']
        else:
            return user_data['article_url']

    def publish_chats(self, bot: Bot, update: Update, user_data):
        channel = update.message.text
        user_data['channel_name'] = channel
        if channel not in self.config.get_channel_names():
            bot.send_message(chat_id=update.message.chat_id, text="Публикация отменена!")
            return ConversationHandler.END
        else:
            options = [["Yes"], ["No"]]
            bot.send_message(chat_id=update.message.chat_id, text="Подтвердите действие. Отправить статью")
            bot.send_message(chat_id=update.message.chat_id, text=self.get_text(user_data))
            bot.send_message(chat_id=update.message.chat_id, text="в чат {}?".format(channel),
                             reply_markup=ReplyKeyboardMarkup(options, one_time_keyboard=True))
            return Publish.PublishOrCancel

    def publish_final(self, bot: Bot, update: Update, user_data):
        if update.message.text == "Yes":
            bot.send_message(chat_id=self.config.get_channel_id(user_data['channel_name']), text=self.get_text(user_data))
            bot.send_message(chat_id=update.message.chat_id, text="Опубликовано!")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Публикация отменена")
        return ConversationHandler.END

    def publish_cancel(self, bot: Bot, update: Update, user_data):
        bot.send_message(chat_id=update.message.chat_id, text="Публикация отменена!")
        return ConversationHandler.END

    def get_version(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text=self.config.get_version())


def create_handlers(config: Config, admin_filter):
    admin = Admin(config)

    return [
        # - Start command
        CommandHandler(command="start", callback=admin.start, filters=admin_filter),
        # - Version command
        CommandHandler(command="version", callback=admin.get_version, filters=admin_filter),

        # - Incoming contact details
        ConversationHandler(
            entry_points=[CommandHandler(command="publish", callback=admin.publish_request, filters=admin_filter)],
            states={
                Publish.GetUrl: [MessageHandler(filters=Filters.text, callback=admin.publish_url, pass_user_data=True)],
                Publish.AddComments: [MessageHandler(callback=admin.publish_comments, pass_user_data=True, filters=Filters.text)],
                Publish.ChooseChats: [MessageHandler(callback=admin.publish_chats, pass_user_data=True, filters=Filters.text)],
                Publish.PublishOrCancel: [MessageHandler(filters=Filters.text, callback=admin.publish_final, pass_user_data=True)],
            },
            fallbacks=[CommandHandler("cancel", callback=admin.publish_cancel)]
        )
    ]
