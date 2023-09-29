from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from config import SERVERS, SUPPORT_BOT_LINK
from db.access_keys import get_keys_by_user, get_key_by_id


def get_main_menu_kb():
    buttons=[]
    ikb = InlineKeyboardMarkup(row_width=2)
    button = InlineKeyboardButton(text='🆓 Пробный период', callback_data='start_trial')
    buttons.append(button)
    button = InlineKeyboardButton(text='💵 Подписка', callback_data='subscribe')
    buttons.append(button)
    button = InlineKeyboardButton(text='📖 Инструкция', callback_data='get_instructions')
    buttons.append(button)
    button = InlineKeyboardButton(text='🔑 Мои ключи', callback_data='my_keys')
    buttons.append(button)
    button = InlineKeyboardButton(text='🆘 Техподдержка', url=f'{SUPPORT_BOT_LINK}')
    buttons.append(button)
    ikb.add(*buttons)
    return ikb


def get_servers_kb():
    ikb = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for srv in SERVERS:
        for price in srv.get("price"):
            button = InlineKeyboardButton(
                text=f'{srv.get("flag")} {srv.get("country")}, {price.get("name_ru")} = {price.get("price")}р',
                callback_data=f'get_new_key {srv.get("name")} {price.get("id")}')
            buttons.append(button)

    ikb.add(*buttons)
    return ikb


def get_extend_period_kb(key, srv):
    ikb = InlineKeyboardMarkup(row_width=1)
    buttons = []
    for price in srv.get("price"):
        button = InlineKeyboardButton(
            text=f'{price.get("name_ru")} = {price.get("price")}р',
            callback_data=f'extend_key {key.id} {price.get("id")}')
        buttons.append(button)

    ikb.add(*buttons)
    return ikb


def get_keys_by_user_kb(chat_id):
    ikb = InlineKeyboardMarkup(row_width=1)
    buttons = []
    keys = get_keys_by_user(chat_id=chat_id, is_trial=False)
    if bool(keys.first()):
        for key in keys:
            due = key.expired.strftime('%d.%m.%Y') if key.expired else '♾'
            button = InlineKeyboardButton(text=f'Ключ №{key.id}, срок действия: {due}',
                                          callback_data=f'prolong_key {key.id}')
            buttons.append(button)
    button = InlineKeyboardButton(text=f'Новый ключ',
                                  callback_data='buy_new_key')
    buttons.append(button)
    ikb.add(*buttons)

    return ikb


def get_extend_kb(key_id):
    ikb = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton('Продлить', callback_data=f'prolong_key {key_id}')
    ikb.add(button)
    return ikb


def get_new_key_kb():
    ikb = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text=f'Новый ключ', callback_data='buy_new_key')
    ikb.add(button)
    return ikb