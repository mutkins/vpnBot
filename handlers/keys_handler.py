from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
import os
import logging
from handlers.common import reset_state
from outline.keys import list_all_keys
log = logging.getLogger("main")
from dotenv import load_dotenv
load_dotenv()

async def add_key(message: types.Message, state: FSMContext):
    # Reset state if it exists
    await reset_state(state=state)
    await message.answer(text='WELCOME MESSAGE')


def decorator(func):
    async def wrapper(message: types.Message):
        if message.from_user.id==os.environ.get('tg_my_id'):
            print('Функция-обёртка!')
            print('Оборачиваемая функция: {}'.format(func))
            print('Выполняем обёрнутую функцию...')
            await func(message)
            print('Выходим из обёртки')
        else:
            print(f"{message.from_user.id} не равно {os.environ.get('tg_my_id')}")
    return wrapper


@decorator
async def list_keys(message: types.Message):
    a = await list_all_keys()
    await message.answer(a)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(add_key, state='*', commands=['add_key'])
    dp.register_message_handler(list_keys, state='*', commands=['list'])