from globals import Base, timestamp, session
from sqlalchemy import Column, Integer, VARCHAR, ForeignKey, DECIMAL, TIMESTAMP


class PictureSize(Base):
    __tablename__ = "sizes"

    id = Column(DECIMAL, primary_key=True)
    pic_id = Column(Integer, ForeignKey("pictures.id"), nullable=False)
    size = Column(VARCHAR(2), nullable=False)
    link = Column(VARCHAR, nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())

    def __init__(self, picture, size, link, **kwargs):
        super(PictureSize, self).__init__(**kwargs)
        self.pic_id = picture.id
        self.size = size
        self.link = link

    def __repr__ (self):
        return f"Picture {self.pic_id} size: {self.size}, link - {self.link}"

    @staticmethod
    def get_by_link(link: str):
        return session.query(PictureSize).filter_by(PictureSize.link == link).first()
    