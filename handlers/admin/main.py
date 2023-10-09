from aiogram import Dispatcher
from handlers.admin.actions import list_keys, add_key, get_log


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(get_log, state='*', commands=['log'])
    dp.register_message_handler(list_keys, state='*', commands=['list'])
    dp.register_message_handler(add_key, state='*', commands=['add_key'])