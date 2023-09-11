from aiogram import types
from outline.keys import list_all_keys
from handlers.other.check_permissions import check_admin_rights
import json


@check_admin_rights
async def list_keys(message: types.Message):
    a = await list_all_keys()
    await message.answer(json.dumps(a, indent=4))

