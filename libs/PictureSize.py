from globals import Base, timestamp, session
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, TIMESTAMP


class PictureSize(Base):
    __tablename__ = "sizes"

    id = Column(Integer, autoincrement=True, primary_key=True)
    pic_id = Column(Integer, ForeignKey("pictures.id"), nullable=False)
    size = Column(VARCHAR(2), nullable=False)
    link = Column(VARCHAR, nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())
    # raw = Column(LargeBinary, nullable=True, default=None)

    def __init__(self, picture_id, size, link, raw=None, **kwargs):
        super(PictureSize, self).__init__(**kwargs)
        self.pic_id = picture_id
        self.size = size
        self.link = link
        self.raw = raw
        self.add_time = timestamp()

    def __repr__(self):
        return f"Picture {self.pic_id} size: {self.size}, link - {self.link}"

    @staticmethod
    def get_by_link(link: str, local_session=session):
        return local_session.query(PictureSize).filter(PictureSize.link == link).first()

    @staticmethod
    def get_sizes_for_id(id: int, local_session=session) -> list:
        return list(map(lambda x: x[0], local_session.query(PictureSize.size).filter(PictureSize.pic_id == id).all()))

    @staticmethod
    def get_all(local_session=session) -> list['PictureSize']:
        return local_session.query(PictureSize).all()