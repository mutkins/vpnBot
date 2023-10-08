from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, UniqueConstraint, exc, DateTime, ForeignKey, Date
from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import logging
from sqlalchemy.types import Boolean
from db.db_init import Base, engine
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta


logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


class AccessKeys(Base):
    __tablename__ = 'AccessKeys'
    id = Column(Integer, primary_key=True)
    server_id = Column(Integer)
    name = Column(String(250))
    password = Column(String(250))
    port = Column(String(250))
    method = Column(String(250))
    chat_id = Column(String(250), ForeignKey("Users.chat_id"), unique=False)
    access_url = Column(String(250), unique=True)
    server_name = Column(String(250))
    date_created = Column(Date)
    is_trial = Column(Boolean)
    expired = Column(Date)
    is_active = Column(Boolean)

    def __init__(self, server_id, chat_id, access_url, server_name, name=None, password=None, port=None, method=None, is_trial=None, expired=None):
        self.server_id = server_id
        self.chat_id = chat_id
        self.name = name
        self.password = password
        self.port = port
        self. method = method
        self.server_name = server_name
        self.date_created = datetime.now()
        self.is_trial = is_trial
        self.expired = expired # datetime.now() + timedelta(days=30) if is_trial else None
        self.is_active = False
        self.access_url = access_url


def add_key_to_db(chat_id, access_key, server_name, is_trial=None, expired=None):
    new_key = AccessKeys(server_id=access_key.get('id'), chat_id=chat_id, access_url=access_key.get('accessUrl'),
                         name=access_key.get('name'), password=access_key.get('password'),
                         port=access_key.get('port'), method=access_key.get('method'), is_trial=is_trial,
                         server_name=server_name, expired=expired)

    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            session.add(new_key)
            session.commit()
            return new_key.id
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def extend_key(key_id, period):
    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            key = session.query(AccessKeys).filter_by(id=key_id).one()
            key.expired += relativedelta(months=int(period))
            session.commit()
            return None
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def get_keys_by_user(chat_id, is_active=None, is_trial=None):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            res = session.query(AccessKeys).filter_by(chat_id=chat_id)
            if is_active is not None:
                res = res.filter_by(is_active=is_active)
            if is_trial is not None:
                res = res.filter_by(is_trial=is_trial)
            return res

        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def do_user_have_active_trial(chat_id):
    keys = get_keys_by_user(chat_id=chat_id)
    if bool(keys.first()):
        for key in keys:
            if key.is_trial:
                return True
    return False


def get_all_active_keys():
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            return session.query(AccessKeys).filter_by(is_active=True)
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def get_key_by_id(key_id):
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            return session.query(AccessKeys).filter_by(id=key_id).one()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def mark_expired_key(key_id):
    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            key = session.query(AccessKeys).filter_by(id=key_id).one()
            key.is_active = False
            session.commit()
            return None
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def activate_key(key_id):
    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            key = session.query(AccessKeys).filter_by(id=key_id).one()
            key.is_active = True
            session.commit()
            return None
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e