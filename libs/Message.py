from globals import Base, timestamp
from sqlalchemy import Column, DECIMAL, Integer, VARCHAR, TIMESTAMP, ForeignKey

# Message with picture
class Message(Base):

    id = Column(DECIMAL, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pic_id = Column(Integer, ForeignKey('pictures.id'), nullable=False)

    def __init__ (self, user_id, picture, **kwargs):
        super(Message, self).__init__(**kwargs)