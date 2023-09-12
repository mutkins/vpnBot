from aiogram import types
from handlers.other.common import reset_state
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from keyboards.keyboards import *
from handlers.user.send_key import *
from db.users import get_user_by_chat_id, add_user
from outline.keys import add_new_key
from db.access_keys import add_key, do_user_have_active_trial


async def send_welcome(message: types.Message, state: FSMContext):
    # Reset state if it exists
    await reset_state(state=state)
    file = InputFile("content/main-menu.png")
    await message.answer_photo(photo=file, caption='Ducky не будет тебя утомлять, выбирай:\n'
                                                   '- Активировать пробный период на <b>30 дней (ого!)</b> в один клик\n'
                                                   '- Оформить подписку <b>всего за 100р/мес</b>\n'
                                                   '- Ознакомиться с правилами и особенностями\n'
                                                   '- Просмотреть свои ключи'
                                                   '', parse_mode='HTML', reply_markup=get_main_meny_kb())


async def start_trial(message: types.Message, state: FSMContext):
    user = get_user_by_chat_id(chat_id=message.from_user.id)
    if not user:
        add_user(chat_id=message.from_user.id, username=message.from_user.username)
    if do_user_have_active_trial(chat_id=message.from_user.id):
        await bot.send_message(text='Вы уже активировали пробный период. Узнать свой ключ и срок действия: /my_key', chat_id=message.from_user.id)
    else:
        access_key = await add_new_key(name=message.from_user.username)
        add_key(chat_id=message.from_user.id, access_key=access_key, is_trial=True)
        await send_key_to_user(chat_id=message.from_user.id, access_url=access_key)
