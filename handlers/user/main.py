from aiogram import Dispatcher
from handlers.user.user_menu import *


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, state='*', commands=['start', 'старт'])
    dp.register_callback_query_handler(start_trial, text=['start_trial'])
    dp.register_callback_query_handler(my_keys, text=['my_keys'])
    dp.register_message_handler(my_keys, state='*', commands=['my_keys'])
    dp.register_message_handler(get_instructions, state='*', commands=['get_instructions'])
    dp.register_callback_query_handler(get_instructions, text=['get_instructions'])
    dp.register_callback_query_handler(get_rules, text=['rules'])
    dp.register_message_handler(get_rules, state='*', commands=['rules'])