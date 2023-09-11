from aiogram import Dispatcher
from handlers.user.add import add_key


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(add_key, state='*', commands=['add'])
