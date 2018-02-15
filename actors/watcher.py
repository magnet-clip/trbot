from telegram import Bot, Update
from telegram.ext import MessageHandler, Filters


def new_chat_members(bot: Bot, update: Update):
    print("new")
    print(update)
    pass


def left_chat_member(bot: Bot, update: Update):
    print("left")
    print(update)
    pass


def create_handlers():
    return [MessageHandler(filters=Filters.status_update.new_chat_members, callback=new_chat_members),
            MessageHandler(filters=Filters.status_update.left_chat_member, callback=left_chat_member)]
