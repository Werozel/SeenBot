from sqlalchemy import Column, Integer, VARCHAR, Binary, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from globals import Base, timestamp, session
from src.comparison import rmsCompare
from libs.PictureSize import PictureSize
from libs.Message import Message

class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(DECIMAL, primary_key=True)
    ups = Column(Integer, default=0)
    downs = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())

    picSize_rel = relationship("PictureSize", backref="picture")
    msg_rel = relationship("Message", backref="picture")

    def __init__ (self, user_id: int, **kwargs):
        super(Picture, self).__init__(**kwargs)
        self.ups = self.downs = 0
        self.user_id = user_id
        self.add_time = timestamp()
    
    def __eq__ (self, other) -> bool:
        return self.link == other.link

    @staticmethod
    def get_by_link(link: str):
        return session.query(Picture).filter_by(Picture.link == link).first()

    @staticmethod
    def get(id: id):
        return session.query(Picture).filter_by(Picture.id == id).first()

    # @staticmethod
    # def was_sent(picture) -> bool:
    #     # FIXME add sizes
    #     res = [pool.apply_async(rmsCompare, args=(i, url,)) for i in list(urls.get(size).keys())]

    def __repr__(self):
        return f"Picture {str(id)}: {str(self.ups)} ups, {str(self.downs)} downs"