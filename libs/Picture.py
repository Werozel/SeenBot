import datetime
from typing import Optional, List

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, String
from sqlalchemy.orm import relationship

from constants import COMMUNITY_ID
from globals import Base, timestamp, session
from libs.PictureSize import PictureSize
from libs.PicMessage import PicMessage

from constants import size_letters

import random


class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key=True)
    ups = Column(Integer, default=0)
    downs = Column(Integer, default=0)
    bads = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    owner_id = Column(Integer, nullable=True)
    access_key = Column(String, nullable=True)
    add_time = Column(TIMESTAMP, default=timestamp())

    picSize_rel = relationship("PictureSize", backref="picture")
    msg_rel = relationship("PicMessage", backref="picture")

    def __init__(self, id: int, user_id: int, owner_id: int, access_key: str, **kwargs):
        super(Picture, self).__init__(**kwargs)
        self.id = id
        self.ups = self.downs = self.bads = 0
        self.user_id = user_id
        self.owner_id = owner_id
        self.access_key = access_key
        self.add_time = timestamp()

    @staticmethod
    def get(id: int, local_session=session):
        return local_session.query(Picture).filter(Picture.id == id).first()

    def get_sizes(self, local_session=session) -> List[PictureSize]:
        return local_session.query(PictureSize).filter(PictureSize.pic_id == self.id).all()

    def get_best_size(self, local_session=session) -> Optional[PictureSize]:
        sizes: List[PictureSize] = self.get_sizes(local_session)
        for size_letter in reversed(size_letters):
            for size in sizes:
                if size.size == size_letter:
                    return size
        return None

    def __repr__(self):
        return f"Picture {str(id)}: {str(self.ups)} ups, {str(self.downs)} downs, {str(self.downs)} bads"

    def to_api_string(self) -> Optional[str]:
        return f"photo{self.owner_id}_{self.id}" if self.owner_id else None

    @staticmethod
    def get_all_ids(local_session=session) -> list:
        return list(map(lambda x: x[0], local_session.query(Picture.id).all()))

    @staticmethod
    def get_pics_count(local_session=session) -> int:
        return len(Picture.get_all_ids(local_session))

    @staticmethod
    def get_random_pic(local_session=session):
        # TODO: Use sql method
        return random.choice(local_session.query(Picture).all())

    @staticmethod
    def get_all_from(start_dt: datetime.datetime, local_session=session) -> List['Picture']:
        # TODO: order asc Picture.ups & order dec Picture.downs + Picture.bads
        return local_session\
            .query(Picture)\
            .filter(
                Picture.add_time > start_dt    # TODO: check if works
            )\
            .order_by(Picture.ups)\
            .limit(10)\
            .all()

    @staticmethod
    def get_best_for_user(user_id, local_session=session) -> List['Picture']:
        # TODO: order asc Picture.ups & order dec Picture.downs + Picture.bads
        return local_session \
            .query(Picture) \
            .filter_by(Picture.user_id == user_id) \
            .order_by(Picture.ups) \
            .limit(10) \
            .all()
