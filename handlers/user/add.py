from aiogram import Bot, Dispatcher, types
from outline.keys import add_new_key


async def add_key(message: types.Message):
    access_url = await add_new_key(message.from_user.username)
    await message.answer(access_url)



