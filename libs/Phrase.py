from globals import Base, timestamp, session
from sqlalchemy import Column, ForeignKey, VARCHAR, TIMESTAMP, Integer
import functools as func
import random


class Phrase(Base):

    __tablename__ = 'phrases'

    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(VARCHAR, nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


    def __init__ (self, text: str, user_id: int, **kwargs):
        super(Phrase, self).__init__(**kwargs)
        self.text = text
        self.user_id = user_id
        self.add_time = timestamp()

    def __repr__(self):
        return f"{self.id}: {self.text}\n"

    @staticmethod
    def get_all_list():
        return list(map(str, session.query(Phrase).all()))

    @staticmethod
    def get_all_str():
        phrase_list = Phrase.get_all_list
        return func.reduce(lambda a, b: a+b, phrase_list) if len(phrase_list) > 0 else ""

    @staticmethod
    def get(phrase_id: int):
        return session.query(Phrase).filter(Phrase.id == phrase_id).first()

    @staticmethod
    def get_random():
        return random.choice(Phrase.get_all_list())