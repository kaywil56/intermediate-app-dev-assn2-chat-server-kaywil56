
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select


Base = declarative_base()


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    to = Column(String)
    coming_from = Column(String)
    msg = Column(String)
  # sent = Column(Integer)


engine = create_engine('sqlite:///messages.db', future=True)
Base.metadata.create_all(engine)

session = Session(engine)


def save_message(going_to, username, message):
    new_message = Message(to=going_to, coming_from=username, msg=message)
    session.add(new_message)
    session.commit()


def get_messages(user):
    msg_list = []
    query = select(Message).where(Message.to == user)
    messages = session.execute(query).scalars()
    for i in messages:
        msg_list.append(i.msg)
    return msg_list