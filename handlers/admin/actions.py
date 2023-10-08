from aiogram import types
from outline.keys import list_all_keys
from handlers.other.check_permissions import check_admin_rights
import json
from db.users import get_user_by_chat_id, add_user
from handlers.user.utils import add_new_key, activate_key, send_active_keys_by_user
from config import TRIAL_SERVER_NAME


@check_admin_rights
async def list_keys(message: types.Message):
    filename = 'temp/keys_list.txt'
    with open(filename, mode='w') as file:
        keys_json = json.dumps(await list_all_keys(), indent=4)
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
