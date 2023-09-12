from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, UniqueConstraint, exc, DateTime, ForeignKey, Date
from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import logging
from sqlalchemy.types import Boolean
from db.db_init import Base, engine
from datetime import datetime


logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


class AccessKeys(Base):
    __tablename__ = 'AccessKeys'
    id = Column(Integer, primary_key=True)
    chat_id = Column(String(250), ForeignKey("Users.chat_id"), unique=False)
    access_key = Column(String(250), unique=True)
    date_created = Column(Date)
    is_trial = Column(Boolean)

    def __init__(self, chat_id, access_key, username=None, is_trial=None):
        self.chat_id = chat_id
        self.username = username
        self.date_created = datetime.now()
        self.is_trial = is_trial
        self.access_key = access_key
        self.is_trial = is_trial


def add_key(chat_id, access_key, is_trial=None):
    new_key = AccessKeys(chat_id=chat_id, access_key=access_key, is_trial=is_trial)

    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            session.add(new_key)
            session.commit()
            return None
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            return e.args


def get_keys_by_user(chat_id):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            return session.query(AccessKeys).filter_by(chat_id=chat_id)
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            return e.args


def do_user_have_active_trial(chat_id):
    keys = get_keys_by_user(chat_id=chat_id)
    if bool(keys.first()):
        for key in keys:
            if key.is_trial:
                return True
    return False
