from aiogram import types
from create_bot import bot
from handlers.user.utils import add_new_key, send_active_keys_by_user, send_instructions
import logging
from Exceptions.Exceptions import *
from dotenv import load_dotenv
import os
from db.access_keys import extend_key
from db.payments import add_payment_to_db
from datetime import datetime, date, timedelta

load_dotenv()
logging.basicConfig(filename="main.log", level=logging.INFO, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


async def send_invoice(chat_id, label, price, payload):

    PRICE = types.LabeledPrice(label=label, amount=price * 100)

    receipt = {"items": [
        {
            "description": label,
            "quantity": "1.00",
            "amount": {
                "value": f"{price}.00",
                "currency": "RUB"
            },
            "vat_code": 1
        }
    ]
    }

    await bot.send_invoice(chat_id=chat_id,
                           title="Подписка",
                           description=f"Vpn ключ, {label}",
                           provider_token=os.environ.get('PAYMENT_TOKEN'),
                           currency="rub",
                           is_flexible=False,
                           prices=[PRICE],
                           start_parameter="one-month-subscription",
                           payload=payload,
                           need_email=True,
                           send_email_to_provider=True,
                           provider_data={
                               "receipt": receipt
                           })


async def pre_checkout_query(pre_checkout_q: types.PreCheckoutQuery):
    if pre_checkout_q.invoice_payload.split(' ')[0] == 'new_key':
        server_name = pre_checkout_q.invoice_payload.split(' ')[1]
        period = pre_checkout_q.invoice_payload.split(' ')[2]
        try:
            await add_new_key(name=pre_checkout_q.from_user.username, chat_id=pre_checkout_q.from_user.id, is_trial=False, server_name=server_name, expired=datetime.now() + timedelta(days=int(period)*30))
            await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
        except Exception as e:
            log.error(f'ERROR with adding new key. Payment canceled {e}')
            await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=False,
                                            error_message='Платеж отменен, попробуйте позже или обратитесь в техподдержку')
    elif pre_checkout_q.invoice_payload.split(' ')[0] == 'extend_key':
        key_id = pre_checkout_q.invoice_payload.split(' ')[1]
        period = pre_checkout_q.invoice_payload.split(' ')[2]
        try:
            extend_key(key_id=key_id, period=period)
            await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=True)
        except Exception as e:
            log.error(f'ERROR with extending key {key_id}. Payment canceled {e}')
            await bot.answer_pre_checkout_query(pre_checkout_q.id, ok=False,
                                            error_message='Платеж отменен, попробуйте позже или обратитесь в техподдержку')
    else:
        raise Exception


async def successful_payment(message: types.Message):
    log.info("SUCCESSFUL PAYMENT:")
    payment_info = message.successful_payment.to_python()
    for k, v in payment_info.items():
        log.info(f"{k} = {v}")
    add_payment_to_db(
        chat_id=message.from_user.id,
        currency=payment_info.get('currency'),
        total_amount=payment_info.get('total_amount'),
        invoice_payload=payment_info.get('invoice_payload'),
        telegram_payment_charge_id=payment_info.get('telegram_payment_charge_id'),
        provider_payment_charge_id=payment_info.get('provider_payment_charge_id'),
        email=payment_info.get('order_info').get('email'),
        phone=payment_info.get('order_info').get('phone'))

    await send_instructions(chat_id=message.from_user.id)
    await send_active_keys_by_user(chat_id=message.from_user.id)
