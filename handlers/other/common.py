from aiogram.dispatcher import FSMContext


async def reset_state(state: FSMContext):
    # Cancel state if it exists
    current_state = await state.get_state()
    if current_state:
        await state.finish()

