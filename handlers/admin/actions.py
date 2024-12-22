from aiogram import types

import config
from outline.keys import list_all_keys
from handlers.other.check_permissions import check_admin_rights
import json
from db.users import get_user_by_chat_id, add_user, get_all_users
from handlers.user.utils import add_new_key, activate_key, send_active_keys_by_user, send_message_for_bot_owner
from config import TRIAL_SERVER_NAME
from create_bot import bot


@check_admin_rights
async def list_keys(message: types.Message):
    for server in config.SERVERS:
        filename = f'temp/keys_list_{server.get("name")}.txt'
        with open(filename, mode='w') as file:
            keys_json = json.dumps(await list_all_keys(server_name=server.get("name")), indent=4)
            file.write(str(keys_json))
        file = types.InputFile(filename)
        await message.answer_document(file)


@check_admin_rights
async def add_key(message: types.Message):
    user = get_user_by_chat_id(chat_id=message.from_user.id)
    if not user:
        add_user(chat_id=message.from_user.id, username=message.from_user.username)
    key_id = await add_new_key(name=message.text, chat_id=message.from_user.id, is_trial=True,
                               server_name=TRIAL_SERVER_NAME, expired=None)
    activate_key(key_id=key_id)
    await send_active_keys_by_user(chat_id=message.from_user.id)


@check_admin_rights
async def get_log(message: types.Message):
    file = types.InputFile('main.log')
    await message.answer_document(file)
    await send_message_for_bot_owner(text=f"Админ запросил лог")


@check_admin_rights
async def send_service_notification(message: types.Message):
    users = get_all_users()
    for user in users:
        await bot.send_message(chat_id=user.chat_id,
                               text='У некоторых пользователей могут наблюдаться проблемы с vpn сервисом.\n'
                                    'Скоро всё починим! 🛠️')


@check_admin_rights
async def send_custom_notification(message: types.Message):
    users = get_all_users()
    for user in users:
        await bot.send_message(chat_id=user.chat_id, text=message.html_text)


@check_admin_rights
async def send_custom_notification_test(message: types.Message):
    await send_message_for_bot_owner(text=message.get_args())
