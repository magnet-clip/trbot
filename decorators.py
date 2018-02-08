def log_member(func):
    def logged_function(*args):
        self = args[0]
        bot = args[1]
        update = args[2]

        user_info = update.effective_user
        message = "User {} ({} {}) with id {} said {}".format(user_info.username, user_info.first_name,
                                                              user_info.last_name, user_info.id,
                                                              update.message.text)
        bot.send_message(chat_id=update.message.chat_id, text=message)
        func(self, bot, update)
    return logged_function


def log_method(func):
    def logged_function(*args):
        bot = args[0]
        update = args[1]

        user_info = update.effective_user
        message = "User {} ({} {}) with id {} said {}".format(user_info.username, user_info.first_name,
                                                              user_info.last_name, user_info.id,
                                                              update.message.text)
        bot.send_message(chat_id=update.message.chat_id, text=message)
        func(bot, update)
    return logged_function

# def log_user(member=True):
#     def logging_function(func):
#         def logged_function(*args):
#             if member:
#                 self = args[0]
#                 bot = args[1]
#                 update = args[2]
#             else:
#                 self = None
#                 bot = args[0]
#                 update = args[1]
#
#             user_info = update.effective_user
#             message = "User {} ({} {}) with id {} said {}".format(user_info.username, user_info.first_name,
#                                                                   user_info.last_name, user_info.id,
#                                                                   update.message.text)
#             bot.send_message(chat_id=update.message.chat_id, text=message)
#             if member:
#                 func(self, bot, update)
#             else:
#                 func(bot, update)
#         return logged_function
#     return logging_function
