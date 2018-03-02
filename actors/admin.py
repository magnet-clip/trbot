from telegram import Bot, Update, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ConversationHandler, CommandHandler, Filters, MessageHandler, InlineQueryHandler, \
    CallbackQueryHandler

from config import Config
from helpers.trkd import TRKD


class Publish:
    GetUrl, AddComments, ChooseChats, PublishOrCancel = range(4)


class Distribute:
    PublishOrCancel, Send = range(2)


class Admin:
    def __init__(self, config: Config, trkd: TRKD):
        self.trkd = trkd
        self.config = config

    def start(self, bot: Bot, update: Update):
        options = [[InlineKeyboardButton(text="Опубликовать статью", callback_data="publish")],
                   [InlineKeyboardButton(text="Разослать рики", callback_data="rics")]]
        bot.send_message(chat_id=update.message.chat_id, text="Выберите команду",
                         reply_markup=InlineKeyboardMarkup(options, one_time_keyboard=True))

    def received_contact(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="Contact")

    def process(self, bot: Bot, update: Update):
        bot.send_message(chat_id=update.message.chat_id, text="Yo admin")

    def publish_request(self, bot: Bot, update: Update):
        """Fist step for publishing"""
        if update.message is not None:
            chat_id = update.message.chat_id
        elif update.effective_message is not None:
            chat_id = update.effective_message.chat_id
        else:
            return ConversationHandler.END
        bot.send_message(chat_id=chat_id, text="Скопируйте сюда сслылку на статью для публикации")
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

    def distribute_request(self, bot: Bot, update: Update):
        chats = list(map(lambda x: [x], self.config.get_channel_names()))
        chats.append(["Cancel"])
        markup = ReplyKeyboardMarkup(chats, one_time_keyboard=True)

        if update.message is not None:
            chat_id = update.message.chat_id
        elif update.effective_message is not None:
            chat_id = update.effective_message.chat_id
        else:
            return ConversationHandler.END

        bot.send_message(chat_id=chat_id, text="В какой чат отправить рассылку?", reply_markup=markup)

        return Distribute.PublishOrCancel

    def distribute_show_and_confirm(self, bot: Bot, update: Update, user_data):
        channel = update.message.text
        user_data['channel_name'] = channel
        if channel not in self.config.get_channel_names():
            bot.send_message(chat_id=update.message.chat_id, text="Рассылка отменена!")
            return ConversationHandler.END
        else:
            # todo fetch rics and create array; store to user_data; send now to admin to confirm
            rics = self.config.get_channel_by_name(channel).get_publications()[0].get_rics()

            ric_names = list(map(lambda x: x.ric, rics))
            quotes = self.trkd.getQuotesList(ric_names)
            for item in quotes['ItemResponse']:
                for element in item['Item']:
                    print("===============")
                    ric = element['RequestKey']['Name']
                    print(ric)
                    for nibble in element['Fields']['Field']:
                        data_type = nibble['DataType']
                        print(nibble['Name'], data_type, nibble[data_type])

            if quotes is not None:
                bot.send_message(chat_id=update.message.chat_id, text="Подтвердите действие. Отправить рассылку")
                bot.send_message(chat_id=update.message.chat_id, text=ric_names)
                bot.send_message(chat_id=update.message.chat_id, text="в чат {}?".format(channel),
                                 reply_markup=ReplyKeyboardMarkup([["Yes"], ["No"]], one_time_keyboard=True))

                return Distribute.Send
            else:
                bot.send_message(chat_id=update.message.chat_id, text="Не удалось получить котировки! Попробуйте снова")
                return ConversationHandler.END

    def distribute_finally(self, bot: Bot, update: Update, user_data):
        if update.message.text == "Yes":
            bot.send_message(chat_id=self.config.get_channel_id(user_data['channel_name']), text="Test")
            bot.send_message(chat_id=update.message.chat_id, text="Разослано!")
        else:
            bot.send_message(chat_id=update.message.chat_id, text="Рассылка отменена!")
        return ConversationHandler.END

    def distribute_cancel(self, bot: Bot, update: Update, user_data):
        bot.send_message(chat_id=update.message.chat_id, text="Рассылка отменена!")
        return ConversationHandler.END


def create_handlers(config: Config, trkd: TRKD, admin_filter):
    admin = Admin(config, trkd)

    return [
        # - Start command
        CommandHandler(command="start", callback=admin.start, filters=admin_filter),
        # - Version command
        CommandHandler(command="version", callback=admin.get_version, filters=admin_filter),

        ConversationHandler(
            entry_points=[CommandHandler(command="rics", callback=admin.distribute_request, filters=admin_filter),
                          CallbackQueryHandler(pattern="rics", callback=admin.distribute_request)],
            states={
                Distribute.PublishOrCancel: [
                    MessageHandler(filters=Filters.text, callback=admin.distribute_show_and_confirm, pass_user_data=True)],
                Distribute.Send: [
                    MessageHandler(filters=Filters.text, callback=admin.distribute_finally, pass_user_data=True)],

            },
            fallbacks=[CommandHandler("cancel", callback=admin.distribute_cancel)]
        ),

        # - Incoming contact details
        ConversationHandler(
            entry_points=[CommandHandler(command="publish", callback=admin.publish_request, filters=admin_filter),
                          CallbackQueryHandler(pattern="publish", callback=admin.distribute_request)],
            states={
                Publish.GetUrl: [MessageHandler(filters=Filters.text, callback=admin.publish_url, pass_user_data=True)],
                Publish.AddComments: [MessageHandler(callback=admin.publish_comments, pass_user_data=True, filters=Filters.text)],
                Publish.ChooseChats: [MessageHandler(callback=admin.publish_chats, pass_user_data=True, filters=Filters.text)],
                Publish.PublishOrCancel: [MessageHandler(filters=Filters.text, callback=admin.publish_final, pass_user_data=True)],
            },
            fallbacks=[CommandHandler("cancel", callback=admin.publish_cancel)]
        )
    ]
