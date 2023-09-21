from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup,\
    InlineKeyboardButton


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