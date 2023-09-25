from aiogram import types
from create_bot import bot
from handlers.user.utils import add_new_key, send_active_keys_by_user, send_instructions
import logging
from Exceptions.Exceptions import *
from dotenv import load_dotenv
import os
load_dotenv()
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")
from config import PRICES


async def send_subscribe_info(chat_id, period, country):
    match period:
        case '1': label = "подписка на 1 месяц"
        case '3': label = "подписка на 3 месяца"
        case '6': label = "подписка на 6 месяцев"

    PRICE = types.LabeledPrice(label=label, amount=PRICES.get(country).get(f'{period} month')*100)

    await bot.send_invoice(chat_id=chat_id,
                           title="Подписка",
                           description=f"Vpn ключ, {label}",
                           provider_token=os.environ.get('PAYMENT_TOKEN'),
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload="test-invoice-payload")


async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    try:
        await add_new_key(name=pre_checkout_q.from_user.username, chat_id=pre_checkout_q.from_user.id, is_trial=False)
        await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
    except Exception as e:
        log.error(f'ERROR with adding new key. Payment canceled {e}')
        await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=False,
                                            error_message='Платеж отменен, попробуйте позже или обратитесь в техподдержку')


async def successful_payment(message: types.Message):
    log.info("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        log.info(f"{k} = {v}")
    await send_instructions(chat_id=message.from_user.id)
    await send_active_keys_by_user(chat_id=message.from_user.id)