from aiogram import Dispatcher
from handlers.admin.actions import list_keys


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(list_keys, state='*', commands=['list'])