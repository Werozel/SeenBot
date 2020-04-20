from globals import Base, timestamp
from sqlalchemy import Column, DECIMAL, Integer, VARCHAR, TIMESTAMP, ForeignKey

# Message with picture
class PicMessage(Base):
    __tablename__ = 'messages'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    pic_id = Column(Integer, ForeignKey('pictures.id'), nullable=False)
    time = Column(TIMESTAMP, default=timestamp())
    text = Column(VARCHAR, default='')

    def __init__ (self, user_id, picture_id, text='', **kwargs):
        super(PicMessage, self).__init__(**kwargs)
        self.user_id = user_id
        self.pic_id = picture_id
        self.time = timestamp()
        self.text = text