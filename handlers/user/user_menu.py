import logging
from datetime import datetime, date, timedelta
from aiogram import types
from handlers.other.common import reset_state
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from keyboards.keyboards import *
from handlers.user.utils import *
from db.users import get_user_by_chat_id, add_user
from handlers.user.utils import add_new_key, get_price_by_period, get_server_by_name
from db.access_keys import do_user_have_active_trial, get_key_by_id
from handlers.user.payment import send_invoice
from config import TRIAL_SERVER_NAME

logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def send_welcome(message: types.Message, state: FSMContext):
    try:
        # Reset state if it exists
        await reset_state(state=state)
        file = InputFile("content/main-menu.png")
        await message.answer_photo(photo=file, caption='Ducky - это просто!\n'
                                                       '- Пробный период на <b>30 дней (ого!)</b> в один клик\n'
                                                       '- Подписка <b>всего за 100р/мес</b>\n'
                                                       '', parse_mode='HTML', reply_markup=get_main_menu_kb())
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)


async def start_trial(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    try:
        user = get_user_by_chat_id(chat_id=call.from_user.id)
        if not user:
            add_user(chat_id=call.from_user.id, username=call.from_user.username)
        if do_user_have_active_trial(chat_id=call.from_user.id):
            await bot.send_message(text='Вы уже активировали пробный период. Узнать свой ключ и срок действия: /my_keys', chat_id=call.from_user.id)
        else:
            await add_new_key(name=call.from_user.username, chat_id=call.from_user.id, is_trial=True,
                              server_name=TRIAL_SERVER_NAME, expired=datetime.now() + timedelta(days=30))
            await send_instructions(chat_id=call.from_user.id)
            await send_active_keys_by_user(chat_id=call.from_user.id)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=call.from_user.id)


async def my_keys(message: types.Message):
    try:
        # If it's callback - send empty answer to finish callback progress bar
        if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
            await message.answer()
        await send_active_keys_by_user(chat_id=message.from_user.id)
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


async def subscription(message: types.Message):
    # If it's callback - send empty answer to finish callback progress bar
    if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
        await message.answer()
    try:
        await send_extend_or_new_key(chat_id=message.from_user.id)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)


async def choose_server_and_rate(message: types.Message):
    # If it's callback - send empty answer to finish callback progress bar
    if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
        await message.answer()
    try:
        await send_servers_and_rates(chat_id=message.from_user.id)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)


async def get_new_key(message: types.Message):
    # If it's callback - send empty answer to finish callback progress bar
    if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
        await message.answer()
    srv_name = message.data.split(' ')[1]
    srv = await get_server_by_name(srv_name=srv_name)
    period = message.data.split(' ')[2]
    price = await get_price_by_period(srv=srv, period=period)
    try:
        await send_invoice(chat_id=message.from_user.id, label=price.get('desc_new_key'), price=price.get('price'), payload=f'new_key {srv_name} {period}')
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)


async def choose_rate(message: types.Message):
    # If it's callback - send empty answer to finish callback progress bar
    if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
        await message.answer()
    key_id = message.data.split(' ')[1]
    try:
        await send_rates(chat_id=message.from_user.id, key_id=key_id)
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)


async def extend_key(message: types.Message):
    # If it's callback - send empty answer to finish callback progress bar
    if str(type(message)) == "<class 'aiogram.types.callback_query.CallbackQuery'>":
        await message.answer()
    key_id = message.data.split(' ')[1]
    period = message.data.split(' ')[2]
    key = get_key_by_id(key_id=key_id)
    srv = await get_server_by_name(key.server_name)
    price = await get_price_by_period(srv=srv, period=period)
    try:
        await send_invoice(chat_id=message.from_user.id, label=price.get('desc_extend_key'), price=price.get('price'), payload=f'extend_key {key_id} {period}')
    except Exception as e:
        log.error(e)
        await send_error_msg(chat_id=message.from_user.id)

