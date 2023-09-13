from aiogram import types
from outline.keys import list_all_keys
from handlers.other.check_permissions import check_admin_rights
import json


@check_admin_rights
async def list_keys(message: types.Message):
    filename = 'temp/keys_list.txt'
    with open(filename, mode='w') as file:
        keys_json = json.dumps(await list_all_keys(), indent=4)
        file.write(str(keys_json))
    file = types.InputFile(filename)
    await message.answer_document(file)

