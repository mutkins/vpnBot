from aiogram import Dispatcher
from handlers.admin.actions import list_keys, add_key, get_log, send_service_notification, send_custom_notification, \
    send_custom_notification_test


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(send_service_notification, state='*', commands=['service'])
    dp.register_message_handler(get_log, state='*', commands=['log'])
    dp.register_message_handler(list_keys, state='*', commands=['list'])
    dp.register_message_handler(add_key, state='*', commands=['add_key'])
    dp.register_message_handler(send_custom_notification, state='*', commands=['message'])
    dp.register_message_handler(send_custom_notification_test, state='*', commands=['test_message'])

