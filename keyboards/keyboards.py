from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton
from config import PRICES
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
    button = InlineKeyboardButton(text=f'🇫🇮 Finland, 1 месяц = {PRICES.get("Finland").get("1 month")}р',
                                  callback_data='Finland 1')
    ikb.add(button)
    button = InlineKeyboardButton(text=f'🇫🇮 Finland, 3 месяца = {PRICES.get("Finland").get("3 month")}р',
                                  callback_data=f'Finland 3')
    ikb.add(button)
    return ikb


def get_keys_by_user_kb(chat_id):
    ikb = InlineKeyboardMarkup(row_width=1)
    buttons = []
    keys = get_keys_by_user(chat_id=chat_id, is_trial=False)
    if bool(keys.first()):
        for key in keys:
            due = key.expired.strftime('%d.%m.%Y') if key.expired else '♾'
            button = InlineKeyboardButton(text=f'Ключ №{key.id}, срок действия: {due}',
                                          callback_data=key.id)
            buttons.append(button)
        button = InlineKeyboardButton(text=f'Новый ключ',
                                      callback_data='buy_new_key')
        buttons.append(button)
        ikb.add(*buttons)

    return ikb