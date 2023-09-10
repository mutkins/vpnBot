from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
import logging

log = logging.getLogger("main")


async def send_welcome(message: types.Message, state: FSMContext):
    # Reset state if it exists
    await reset_state(state=state)
    await message.answer(text='WELCOME MESSAGE')


async def reset_state(state: FSMContext):
    # Cancel state if it exists
    current_state = await state.get_state()
    if current_state:
        await state.finish()


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(send_welcome, state='*', commands=['cancel', 'отмена', 'start', 'help', 'хелп'])