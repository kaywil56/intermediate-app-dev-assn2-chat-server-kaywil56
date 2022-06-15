
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime


Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    to = Column(String)
    coming_from = Column(String)
    msg = Column(String)
    time_sent = Column(Integer)


engine = create_engine('sqlite:///messages.db', future=True, connect_args={"check_same_thread": False})
Base.metadata.create_all(engine)

session = Session(engine)


def save_message(going_to, username, message):
    time_sent = datetime.utcnow()
    time = time_sent and time_sent.isoformat()

    new_message = Message(to=going_to, coming_from=username, msg=message, time_sent=time)
    session.add(new_message)
    session.commit()


def get_messages(user, last_read):
    msg_list = []
    if last_read is None:
        print("none")
        query = select(Message).where(Message.to == user)
    else:
        query = select(Message).where(Message.to == user).filter(Message.time_sent > last_read)

    messages = session.execute(query).scalars()
    for i in messages:
        msg_list.append(i.msg)
    return msg_list