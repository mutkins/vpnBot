import os
from aiogram import Bot, Dispatcher, types
from aiogram.bot.api import TelegramAPIServer
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
from config import PROXY
storage = MemoryStorage()
load_dotenv()
if PROXY:
    bot = Bot(token=os.environ.get('tgBot_id'), proxy=PROXY)
else:
    bot = Bot(token=os.environ.get('tgBot_id'))
dp = Dispatcher(bot, storage=storage)
