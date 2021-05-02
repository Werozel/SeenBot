from typing import Optional

from globals import Base
from sqlalchemy import Column, String, ForeignKey, Integer
from sqlalchemy.orm import Session

from globals import session


class DownloadedPic(Base):
    __tablename__ = "downloaded_pics"

    id = Column(Integer, primary_key=True)
    album_id = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    access_key = Column(String, nullable=True)

    @staticmethod
    def get(id: int, local_session: Session = session) -> Optional['DownloadedPic']:
        return local_session.query(DownloadedPic).get(id)

    def get_api_str(self):
        return f"photo{self.owner_id}_{self.id}" + (f"_{self.access_key}" if self.access_key else "")
