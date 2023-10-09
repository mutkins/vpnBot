from time import strftime

from create_bot import bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from handlers.user.utils import *
from outline.keys import add_key_to_srv, delete_key
from db.access_keys import *
import logging
from Exceptions.Exceptions import *
from keyboards.keyboards import get_servers_kb, get_keys_by_user_kb, get_extend_period_kb
from config import SERVERS, SUPPORT_BOT_USERNAME

logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def send_instructions(chat_id):
    log.info('send_instructions')
    file = InputFile("content/manual.png")
    await bot.send_photo(photo=file, caption='Шаг 1: Скачайте приложение\n'
                                '<a href="https://play.google.com/store/apps/details?id=org.outline.android.client">Android</a> | '
                                '<a href="https://itunes.apple.com/app/outline-app/id1356177741">iPhone</a> | '
                                '<a href="https://s3.amazonaws.com/outline-releases/client/windows/stable/Outline-Client.exe">Windows</a> | '
                                '<a href="https://s3.amazonaws.com/outline-releases/client/linux/stable/Outline-Client.AppImage">Linux</a> | '
                                '<a href="https://itunes.apple.com/app/outline-app/id1356178125">macOS</a>\n'
                                'Шаг 2: Скопируйте ключ доступа, который начинается с ss:// и вставьте в приложение\n'
                                'Шаг 3: Подключайтесь и пользуйтесь\n'
                                '<b>ВАЖНО:</b>\n'
                                '🔑 Одним ключом можно пользоваться на всех ваших устройствах.\n'
                                '🚫 Нельзя делиться ключом с другими людьми. В противном случае ключ будет заблокирован\n'
                                , chat_id=chat_id, parse_mode='HTML')


async def send_active_keys_by_user(chat_id):
    log.info('send_active_keys_by_user')
    keys = get_keys_by_user(chat_id=chat_id, is_active=True)
    if bool(keys.first()):
        await bot.send_message(text=f'Ваши активные ключи доступа:', chat_id=chat_id, parse_mode='HTML')
        for key in keys:
            key_type = 'Пробный' if key.is_trial else 'Постоянный'
            due = key.expired.strftime('%d.%m.%Y') if key.expired else '♾'
            await bot.send_message(text=f'<code>{key.access_url}</code> | Ключ №{key.id} | {key_type} | Срок действия {due}', chat_id=chat_id, parse_mode='HTML')
    else:
        await bot.send_message(text=f'У вас нет активных ключей доступа, приобретите подписку или '
                                    f'воспользуйтесь пробным периодом', chat_id=chat_id, parse_mode='HTML')


async def get_keys(message: types.Message):
    await send_instructions(chat_id=message.from_user.id)


async def add_new_key(name, chat_id, server_name, expired, is_trial=False):
    log.info('add_new_key')
    access_key = await add_key_to_srv(name=name)
    try:
        key_id = add_key_to_db(chat_id=chat_id, access_key=access_key, is_trial=is_trial,
                      server_name=server_name, expired=expired)
        return key_id
    except Exception as e:
        log.error(e)
        log.error('Cause ERROR with addind key to db, DELETE key from server')
        await delete_key(access_key.get('id'))
        log.error('Key deleted from server')
        raise e


async def send_error_msg(chat_id):
    log.info('send_error_msg')
    await bot.send_message(text=f'<b>Ошибка, попробуйте позже или обратитесь в техподдержку {SUPPORT_BOT_USERNAME}</b>',
                           chat_id=chat_id, parse_mode='HTML')


async def send_rules(chat_id):
    file = InputFile("content/rules.png")
    await bot.send_photo(photo=file, caption='🔑 Одним ключом можно пользоваться на всех ваших устройствах.\n'
                                             '🚫 Нельзя делиться ключом с другими людьми. В противном случае ключ будет заблокирован\n'
                                             'Вот и всё!', chat_id=chat_id, parse_mode='HTML')


async def send_servers_and_rates(chat_id):
    file = InputFile("content/servers.png")
    await bot.send_photo(photo=file, caption= '<b>Выберите страну для генерации VPN ключа и тариф</b>\n'
                                              'Обратите внимание:\n'
                                              '— Российсие сервера актуальны, если вы находитесь за пределами РФ и вам нужен доступ к российским ресурсам\n'
                                              '— Зарубежные сервера актуальны, если вы находитесь в РФ и вам нужен доступ к зарубежным ресурсам\n'
                                              'Вы всегда можете вернуться в этот раздел и сформировать ключи для других серверов',
                         chat_id=chat_id, parse_mode='HTML', reply_markup=get_servers_kb())


async def send_rates(chat_id, key_id):
    file = InputFile("content/rates.png")
    key = get_key_by_id(key_id=key_id)
    srv = await get_server_by_name(key.server_name)
    await bot.send_photo(photo=file, caption='Выберите тариф для продления',
                         chat_id=chat_id, parse_mode='HTML', reply_markup=get_extend_period_kb(key=key, srv=srv))


async def send_extend_or_new_key(chat_id):
    file = InputFile("content/subscribe.png")
    await bot.send_photo(photo=file, caption='Выберите ключ, который хотите продлить, или оформите новый\n'
                                             '<i>Примечание: вы не можете продлить пробный ключ. Если он истек - нужно выпустить новый, постоянный</i>',
                         chat_id=chat_id, parse_mode='HTML', reply_markup=get_keys_by_user_kb(chat_id=chat_id))


async def get_server_by_name(srv_name):
    for srv in SERVERS:
        if srv.get('name') == srv_name:
            return srv
    return None


async def get_price_by_period(srv, period):
    for price in srv.get('price'):
        if price.get('id') == int(period):
            return price
    return None