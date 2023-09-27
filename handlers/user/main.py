from aiogram import Dispatcher
from handlers.user.user_menu import *
from aiogram.types.message import ContentType
from handlers.user.payment import pre_checkout_query, successful_payment


def register_user_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, state='*', commands=['start', 'старт'])
    dp.register_callback_query_handler(start_trial, text=['start_trial'])
    dp.register_callback_query_handler(my_keys, text=['my_keys'])
    dp.register_message_handler(my_keys, state='*', commands=['my_keys'])
    dp.register_message_handler(get_instructions, state='*', commands=['get_instructions'])
    dp.register_callback_query_handler(get_instructions, text=['get_instructions'])
    dp.register_callback_query_handler(get_rules, text=['rules'])
    dp.register_message_handler(get_rules, state='*', commands=['rules'])
    dp.register_callback_query_handler(subscription, text=['subscribe'])
    dp.register_message_handler(subscription, state='*', commands=['subscribe'])
    dp.register_callback_query_handler(choose_server_and_rate, text=['buy_new_key'])
    dp.register_callback_query_handler(choose_rate, lambda callback: callback.data.startswith('prolong_key'))
    dp.register_callback_query_handler(extend_key, lambda callback: callback.data.startswith('extend_key'))
    dp.register_callback_query_handler(get_new_key, lambda callback: callback.data.startswith('get_new_key'))
    dp.register_message_handler(successful_payment, content_types=ContentType.SUCCESSFUL_PAYMENT)
    dp.register_pre_checkout_query_handler(pre_checkout_query, lambda message: True)

