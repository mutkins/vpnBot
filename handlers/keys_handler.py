from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
import os
import logging
from handlers.other.common import reset_state
from outline.keys import list_all_keys
log = logging.getLogger("main")
from dotenv import load_dotenv
load_dotenv()

async def add_key(message: types.Message, state: FSMContext):
    # Reset state if it exists
    await reset_state(state=state)
    await message.answer(text='WELCOME MESSAGE')


def check_admin_rights(func):
    async def wrapper(message: types.Message):
        if str(message.from_user.id) == str(os.environ.get('my_chat_id')):
            print('Функция-обёртка!')
            print('Оборачиваемая функция: {}'.format(func))
            print('Выполняем обёрнутую функцию...')
            await func(message)
            print('Выходим из обёртки')
        else:
            print(f"{message.from_user.id} не равно {os.environ.get('my_chat_id')}")
            a = message.from_user.id
            b = os.environ.get('my_chat_id')
            print(type(a), type(b))
    return wrapper


@check_admin_rights
async def list_keys(message: types.Message):
    a = await list_all_keys()
    await message.answer(a)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(add_key, state='*', commands=['add_key'])
    dp.register_message_handler(list_keys, state='*', commands=['list'])