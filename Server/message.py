""" This file handles saving and retreiving from the database """

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime


Base = declarative_base()


class Message(Base):
    """A message table for the sqlite DB"""
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    to = Column(String)
    coming_from = Column(String)
    msg = Column(String)
    time_sent = Column(Integer)


engine = create_engine('sqlite:///messages.db', future=True,
                       connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)

session = Session(engine)


def save_message(going_to, username, message):
    """For saving messages in the sqlite DB"""
    time_sent = datetime.utcnow()
    time = time_sent and time_sent.isoformat()
    print('message: ' + message)
    print('going to: ' + going_to)
    if len(message) == 0 or len(going_to) == 0:
        raise Exception('You cant leave fields empty.')
    else:
        new_message = Message(
            to=going_to, coming_from=username, msg=message, time_sent=time)
        session.add(new_message)
        session.commit()


def get_messages(user, last_read):
    """For retreiving messages in the sqlite DB"""
    msg_list = []
    if last_read is None:
        query = select(Message).where(Message.to == user)
    else:
        query = select(Message).where(Message.to == user).filter(
            Message.time_sent > last_read)
    messages = session.execute(query).scalars()
    for i in messages:
        msg_list.append(i.msg)
    if len(msg_list) == 0:
        raise Exception('You have no messages.')
    else:
        return msg_list
