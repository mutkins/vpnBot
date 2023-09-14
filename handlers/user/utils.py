from create_bot import bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from handlers.user.utils import *
from outline.keys import add_key_to_srv
from db.access_keys import *
from outline.keys import *
import logging
from Exceptions.Exceptions import *


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
    try:
        add_key_to_db(chat_id=chat_id, access_key=access_key, is_trial=is_trial)
    except Exception as e:
        log.error(e)
        log.error('Cause ERROR with addind key to db, DELETE key from server')
        await delete_key(access_key.get('id'))
        log.error('Key deleted from server')
        raise e


async def send_error_msg(chat_id):
    bot.send_message(text=f'<b>Ошибка, попробуйте позже или обратитесь в техподдержку</b>',
                     chat_id=chat_id, parse_mode='HTML')