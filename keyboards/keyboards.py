from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, \
    InlineKeyboardButton
from config import SERVERS
from db.access_keys import get_keys_by_user


def get_main_menu_kb():
    ikb = InlineKeyboardMarkup(row_width=1)
    button = InlineKeyboardButton(text='🆓 Пробный период', callback_data='start_trial')
    ikb.add(button)
    button = InlineKeyboardButton(text='💵 Подписка', callback_data='subscribe')
    ikb.add(button)
    button = InlineKeyboardButton(text='📄 Правила', callback_data='rules')
    ikb.add(button)
    button = InlineKeyboardButton(text='📖 Инструкция', callback_data='get_instructions')
    ikb.add(button)
    button = InlineKeyboardButton(text='🔑 Мои ключи', callback_data='my_keys')
    ikb.add(button)
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


def get_keys_by_user_kb(chat_id):
    ikb = InlineKeyboardMarkup(row_width=1)
    buttons = []
    keys = get_keys_by_user(chat_id=chat_id, is_trial=False)
    if bool(keys.first()):
        for key in keys:
            due = key.expired.strftime('%d.%m.%Y') if key.expired else '♾'
            button = InlineKeyboardButton(text=f'Ключ №{key.id}, срок действия: {due}',
                                          callback_data=f'extend_key {key.id}')
            buttons.append(button)
    button = InlineKeyboardButton(text=f'Новый ключ',
                                  callback_data='buy_new_key')
    buttons.append(button)
    ikb.add(*buttons)

    return ikb
