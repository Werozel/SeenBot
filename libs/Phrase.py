from globals import Base, timestamp
from sqlalchemy import Column, DECIMAL, ForeignKey, VARCHAR, TIMESTAMP, Integer


class Phrase(Base):

    __tablename__ = 'phrases'

    id = Column(DECIMAL, primary_key=True)
    text = Column(VARCHAR, nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)


    def __init__ (self, text: str, user_id: int, **kwargs):
        super(Phrase, self).__init__(**kwargs)
        self.text = text
        self.user_id = user_id
        self.add_time = timestamp()
