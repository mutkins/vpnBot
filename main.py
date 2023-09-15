from aiogram.utils import executor
from create_bot import dp
from handlers import register_all_handlers
from db.db_init import engine, Base
from keys_checker import on_startup
from create_bot import bot
from aiogram import types

register_all_handlers(dp)
Base.metadata.create_all(engine)


# @dp.pre_checkout_query_handler(lambda query: True)
# async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
#     await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
