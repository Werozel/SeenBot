import os
from typing import List

import wget
from sqlalchemy.orm import Session

import config
from globals import Base, session, timestamp, vk_upload
from sqlalchemy import Column, BigInteger, VARCHAR, ForeignKey, Integer, TIMESTAMP, func


class RawLink(Base):
    __tablename__ = "raw_links"

    id = Column(BigInteger, primary_key=True)
    type = Column(VARCHAR(15), nullable=False)
    owner_id = Column(BigInteger, nullable=False)
    access_key = Column(VARCHAR)
    track_code = Column(VARCHAR, nullable=True)
    url = Column(VARCHAR, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())

    def __init__(
        self,
        id: int,
        type: str,
        owner_id: int,
        access_key: str,
        track_code: str,
        url: str,
        user_id: int,
        **kwargs
    ) -> None:
        super(RawLink, self).__init__(**kwargs)
        self.id = id
        self.type = type
        self.owner_id = owner_id
        self.access_key = access_key
        self.track_code = track_code
        self.url = url
        self.user_id = user_id
        self.add_time = timestamp()

    @staticmethod
    def get(id: int, local_session=session):
        return local_session.query(RawLink).filter(RawLink.id == id).first()

    @staticmethod
    def get_all_with_type(type: str, local_session=session) -> list:
        return local_session.query(RawLink).filter(RawLink.type == type).all()

    @staticmethod
    def get_all(local_session=session) -> List['RawLink']:
        return local_session.query(RawLink).all()

    def get_attachment_string(self) -> str:
        return f"{self.type}{self.owner_id}_{self.id}{ f'_{self.access_key}' if self.access_key else '' }"

    @staticmethod
    def get_random_audio(local_session: Session = session) -> 'RawLink':
        return local_session \
            .query(RawLink) \
            .filter(RawLink.type == 'audio') \
            .filter(RawLink.url != None) \
            .order_by(func.random()) \
            .first()

    def get_api_string(self, peer_id: str) -> str:
        # TODO: cache
        file_name = wget.download(self.url)
        audio_obj: dict = vk_upload.audio_message(file_name, peer_id=peer_id).get('audio_message')
        os.remove(file_name)
        access_key = audio_obj.get('access_key')
        return f"audio_message{audio_obj.get('owner_id')}_{audio_obj.get('id')}" + (f"_{access_key}" if access_key else "")
