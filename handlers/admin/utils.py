import os
from time import strftime

from create_bot import bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from handlers.user.utils import *
from outline.keys import add_key_to_srv
from db.access_keys import *
from outline.keys import *
import logging
from Exceptions.Exceptions import *


async def send_error_report(error_msg):
    await bot.send_message(text=error_msg, chat_id=os.environ.get('my_chat_id'), parse_mode='HTML')