from sqlalchemy import Column, Integer, VARCHAR, Binary, DECIMAL, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from globals import Base, timestamp, session
from src.comparison import rmsCompare
from libs.PictureSize import PictureSize
from libs.PicMessage import PicMessage

class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)
    ups = Column(Integer, default=0)
    downs = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())

    picSize_rel = relationship("PictureSize", backref="picture")
    msg_rel = relationship("PicMessage", backref="picture")

    def __init__ (self, id: int, user_id: int, **kwargs):
        super(Picture, self).__init__(**kwargs)
        self.id = id
        self.ups = self.downs = 0
        self.user_id = user_id
        self.add_time = timestamp()
    
    def __eq__ (self, other) -> bool:
        return self.link == other.link

    @staticmethod
    def get(id: int):
        return session.query(Picture).filter(Picture.id==id).first()

    def get_sizes(self):
        return session.query(PictureSize).filter_by(PictureSize.pic_id == self.id).all()

    def __repr__(self):
        return f"Picture {str(id)}: {str(self.ups)} ups, {str(self.downs)} downs"