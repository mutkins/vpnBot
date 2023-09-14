from aiogram import Dispatcher
from handlers.user.user_menu import *


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, state='*', commands=['start', 'старт'])
    dp.register_callback_query_handler(start_trial, text=['start_trial'])
    dp.register_callback_query_handler(my_keys_c, text=['my_keys'])
    dp.register_message_handler(my_keys_m, state='*', commands=['my_keys'])
    dp.register_message_handler(get_instructions_m, state='*', commands=['get_instructions'])
    dp.register_callback_query_handler(get_instructions_c, text=['get_instructions'])
