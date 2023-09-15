import logging

from aiogram import types
from handlers.other.common import reset_state
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from keyboards.keyboards import *
from handlers.user.utils import *
from db.users import get_user_by_chat_id, add_user
from handlers.user.utils import add_new_key
from db.access_keys import do_user_have_active_trial


logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def send_welcome(message: types.Message, state: FSMContext):
    # Reset state if it exists
    await reset_state(state=state)
    file = InputFile("content/main-menu.png")
    await message.answer_photo(photo=file, caption='Ducky - это просто!\n'
                                                   '- Пробный период на <b>30 дней (ого!)</b> в один клик\n'
                                                   '- Подписка <b>всего за 100р/мес</b>\n'
                                                   '', parse_mode='HTML', reply_markup=get_main_meny_kb())


async def start_trial(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    try:
        user = get_user_by_chat_id(chat_id=call.from_user.id)
        if not user:
            add_user(chat_id=call.from_user.id, username=call.from_user.username)
        if do_user_have_active_trial(chat_id=call.from_user.id):
            await bot.send_message(text='Вы уже активировали пробный период. Узнать свой ключ и срок действия: /my_keys', chat_id=call.from_user.id)
        else:
            await add_new_key(name=call.from_user.username, chat_id=call.from_user.id, is_trial=True)
            await send_instructions(chat_id=call.from_user.id)
            await send_keys_by_user(chat_id=call.from_user.id)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=call.from_user.id)


async def my_keys(message: types.Message):
    # If it's callback - send empty answer to finish callback progress bar
    if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
        await message.answer()
    try:
        await send_keys_by_user(chat_id=message.from_user.id)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)


async def get_instructions(message: types.Message):
    # If it's callback - send empty answer to finish callback progress bar
    if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
        await message.answer()
    try:
        await send_instructions(chat_id=message.from_user.id)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)


async def get_rules(message: types.Message):
    # If it's callback - send empty answer to finish callback progress bar
    if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
        await message.answer()
    try:
        await send_rules(chat_id=message.from_user.id)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)