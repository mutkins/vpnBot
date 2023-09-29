from create_bot import bot
from keyboards.keyboards import get_extend_kb, get_new_key_kb


async def send_expired_msg(chat_id, days_to_expire, key_id):
    match days_to_expire:
        case 3:
            text = f'Ключ {key_id} истечет через 3 дня. Продлите ключ, чтобы сохранить доступ к любимым ресурсам'
            reply_markup = get_extend_kb(key_id=key_id)
        case 2:
            text = f'Ключ {key_id} истечет послезавтра. Продлите ключ, чтобы сохранить доступ к любимым ресурсам'
            reply_markup = get_extend_kb(key_id=key_id)
        case 1:
            text = f'Ключ {key_id} истечет завтра. Продлите ключ, чтобы сохранить доступ к любимым ресурсам'
            reply_markup = get_extend_kb(key_id=key_id)
        case _ if days_to_expire <= 0:
            text = f'Ключ {key_id} истек. Оформите новый, чтобы сохранить доступ к любимым ресурсам'
            reply_markup = get_new_key_kb()
    await bot.send_message(chat_id=chat_id, text=text, reply_markup=reply_markup)
