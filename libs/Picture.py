from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from globals import Base, timestamp, session
from libs.PictureSize import PictureSize
from libs.PicMessage import PicMessage


class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)
    ups = Column(Integer, default=0)
    downs = Column(Integer, default=0)
    bads = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())

    picSize_rel = relationship("PictureSize", backref="picture")
    msg_rel = relationship("PicMessage", backref="picture")

    def __init__(self, id: int, user_id: int, **kwargs):
        super(Picture, self).__init__(**kwargs)
        self.id = id
        self.ups = self.downs = self.bads = 0
        self.user_id = user_id
        self.add_time = timestamp()

    @staticmethod
    def get(id: int, local_session=session):
        return local_session.query(Picture).filter(Picture.id == id).first()

    def get_sizes(self, local_session=session):
        return local_session.query(PictureSize).filter_by(PictureSize.pic_id == self.id).all()

    def __repr__(self):
        return f"Picture {str(id)}: {str(self.ups)} ups, {str(self.downs)} downs, {str(self.downs)} bads"

    @staticmethod
    def get_all_ids(local_session=session) -> list:
        return list(map(lambda x: x[0], local_session.query(Picture.id).all()))

    @staticmethod
    def get_pics_count(local_session=session) -> int:
        return len(Picture.get_all_ids(local_session))


