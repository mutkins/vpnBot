from aiogram.utils import executor
from create_bot import dp
from handlers import register_all_handlers
from db.db_init import engine, Base
from keys_checker import on_startup
register_all_handlers(dp)
Base.metadata.create_all(engine)





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
