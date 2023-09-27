from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, UniqueConstraint, exc, DateTime, ForeignKey, Date
from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import logging
from sqlalchemy.types import Boolean
from db.db_init import Base, engine
from datetime import datetime, date, timedelta
import uuid

logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


class Payments(Base):
    __tablename__ = 'Payments'
    id = Column(String(250), primary_key=True)
    currency = Column(String(250))
    total_amount = Column(String(250))
    invoice_payload = Column(String(250))
    email = Column(String(250))
    phone = Column(String(250))
    telegram_payment_charge_id = Column(String(250))
    provider_payment_charge_id = Column(String(250))
    date_created = Column(DateTime)
    chat_id = Column(String(250), ForeignKey("Users.chat_id"), unique=False)

    def __init__(self, chat_id, currency, total_amount, invoice_payload, telegram_payment_charge_id,
                 provider_payment_charge_id, email=None, phone=None):
        self.id = str(uuid.uuid4())
        self.currency = currency
        self.total_amount = total_amount
        self.invoice_payload = invoice_payload
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id
        self.email = email
        self.phone = phone
        self.date_created = datetime.now()
        self.chat_id = chat_id


def add_payment_to_db(chat_id, currency, total_amount, invoice_payload, telegram_payment_charge_id,
                 provider_payment_charge_id, email=None, phone=None):
    new_payment = Payments(
        chat_id=chat_id,
        currency=currency,
        total_amount=total_amount,
        invoice_payload=invoice_payload,
        telegram_payment_charge_id=telegram_payment_charge_id,
        provider_payment_charge_id=provider_payment_charge_id,
        email=email,
        phone=phone
    )

    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            session.add(new_payment)
            session.commit()
            return None
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e
