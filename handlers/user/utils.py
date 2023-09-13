from aiogram import Bot, Dispatcher, types
from create_bot import bot
from aiogram.types import InputFile
from aiogram import types
from handlers.other.common import reset_state
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from keyboards.keyboards import *
from handlers.user.utils import *
from db.users import get_user_by_chat_id, add_user
from outline.keys import add_key_to_srv
from db.access_keys import add_key_to_db, do_user_have_active_trial, get_keys_by_user
import logging

logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def send_instructions(chat_id):
    file = InputFile("content/manual.png")
    await bot.send_photo(photo=file, caption='<b>Шаг 1: Скачайте приложение</b>\n'
                                '<a href="https://play.google.com/store/apps/details?id=org.outline.android.client">Android</a> | '
                                '<a href="https://itunes.apple.com/app/outline-app/id1356177741">iPhone</a> | '
                                '<a href="https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe">Windows</a> | '
                                '<a href="https://s3.amazonaws.com/outline-releases/client/linux/stable/Outline-Client.AppImage">Linux</a> | '
                                '<a href="https://itunes.apple.com/app/outline-app/id1356178125">macOS</a>\n'
                                '<b>Шаг 2: Скопируйте ключ доступа, который начинается с ss:// и вставьте в приложение</b>\n'
                                '<b>Шаг 3: Подключайтесь и пользуйтесь</b>', chat_id=chat_id, parse_mode='HTML')


async def send_keys_by_user(chat_id):
    keys = get_keys_by_user(chat_id=chat_id)
    if bool(keys.first()):
        await bot.send_message(text=f'<b>Ваши активные ключи доступа:</b>', chat_id=chat_id, parse_mode='HTML')
        for key in keys:
            await bot.send_message(text=f'<code>{key.access_url}</code>\n', chat_id=chat_id, parse_mode='HTML')
    else:
        await bot.send_message(text=f'<b>У вас нет активных ключей доступа, приобретите подписку или '
                                    f'воспользуйтесь пробным периодом</b>', chat_id=chat_id, parse_mode='HTML')


async def get_keys(message: types.Message, state: FSMContext):
    await send_instructions(chat_id=message.from_user.id)


async def add_new_key(name, chat_id, is_trial=False):
    access_key = await add_key_to_srv(name=name)
    add_key_to_db(chat_id=chat_id, access_key=access_key, is_trial=is_trial)
    try:
        verify_consistency()
    except Exception as e:
        log.error(e)


async def verify_consistency():
    pass