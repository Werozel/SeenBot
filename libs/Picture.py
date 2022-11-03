import datetime
from typing import Optional, List

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, String
from sqlalchemy.orm import relationship, Session
from sqlalchemy.sql.expression import func

from globals import Base, timestamp, session, vk_upload
from libs.PictureSize import PictureSize
from libs.DownloadedPic import DownloadedPic

from constants import size_letters

import os
import wget


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
    downloaded_pic_rel = relationship("DownloadedPic", backref='picture')

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

    @staticmethod
    def get_all_ids(local_session=session) -> list:
        return list(map(lambda x: x[0], local_session.query(Picture.id).all()))

    @staticmethod
    def get_all(local_session=session) -> list:
        return local_session.query(Picture).all()

    @staticmethod
    def get_pics_count(local_session=session) -> int:
        return len(Picture.get_all_ids(local_session))

    @staticmethod
    def get_random_pic(local_session: Session = session):
        return local_session \
            .query(Picture) \
            .order_by(func.random()) \
            .first()

    @staticmethod
    def get_all_from_date_ordered(
        start_dt: datetime.datetime,
        local_session: Session = session,
        limit: int = None
    ) -> List['Picture']:
        return local_session\
            .query(Picture)\
            .filter(
                Picture.add_time > start_dt
            )\
            .order_by(
                -(Picture.ups / (Picture.downs + 1)) * (Picture.ups + Picture.downs)
            )\
            .limit(limit)\
            .all()

    @staticmethod
    def get_best_for_user(user_id, local_session: Session = session, limit: int = None) -> List['Picture']:
        return local_session \
            .query(Picture) \
            .filter(Picture.user_id == user_id) \
            .order_by(
                -(Picture.ups / (Picture.downs + 1)) * (Picture.ups + Picture.downs)
            )\
            .limit(limit) \
            .all()

    def get_api_string(self, peer_id: str, local_session=session) -> str:
        downloaded_pic: Optional[DownloadedPic] = DownloadedPic.get_by_pic_id(self.id, local_session)
        if downloaded_pic is None:
            file_name = wget.download(self.get_best_size(local_session).link)
            photo_obj: dict = vk_upload.photo_messages(file_name, peer_id=peer_id)[0]
            os.remove(file_name)
            downloaded_pic = DownloadedPic(
                id=photo_obj.get('id'),
                picture_id=self.id,
                album_id=photo_obj.get('album_id'),
                owner_id=photo_obj.get('owner_id'),
                access_key=photo_obj.get('access_key')
            )
            local_session.add(downloaded_pic)
            local_session.commit()

        return downloaded_pic.get_api_str()
