from aiogram import Dispatcher
from handlers.user.user_menu import *


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_key_to_user, state='*', commands=['add'])
    dp.register_message_handler(send_welcome, state='*', commands=['start', 'старт'])
    dp.register_callback_query_handler(start_trial, text=['start_trial'])