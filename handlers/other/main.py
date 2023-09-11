from aiogram import Dispatcher
from handlers.other.etc import etc


def register_other_handlers(dp: Dispatcher):
    dp.register_message_handler(etc, state='*', commands=['etc'])
