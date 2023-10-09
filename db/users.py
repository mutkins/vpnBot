from sqlalchemy import create_engine, select, Table, Column, Integer, String, MetaData, UniqueConstraint, exc, DateTime
from sqlalchemy.orm import mapper, relationship, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
import logging
from sqlalchemy.types import Boolean
from db.db_init import Base, engine


logging.basicConfig(filename="main.log", level=logging.DEBUG, filemode="w",
                    format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("main")


class Users(Base):
    __tablename__ = 'Users'
    chat_id = Column(String(250), primary_key=True)
    username = Column(String(250), nullable=True)

    def __init__(self, chat_id, username=None):
        self.chat_id = chat_id
        self.username = username


def add_user(chat_id, username=None):
    log.info('add_user')
    new_user = Users(chat_id=chat_id, username=username)

    with Session(engine) as session:
        session.expire_on_commit = False
        try:
            session.add(new_user)
            session.commit()
            return None
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def get_user_by_chat_id(chat_id):
    log.info('get_user_by_chat_id')
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            return session.query(Users).filter_by(chat_id=chat_id).first()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e


def get_all_users():
    log.info('get_all_users')
    with Session(engine) as session:
        # session.expire_on_commit = False
        try:
            return session.query(Users).all()
        except exc.IntegrityError as e:
            # return error if something went wrong
            session.rollback()
            log.error(e)
            raise e
