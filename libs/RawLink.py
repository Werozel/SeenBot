from globals import Base, session, timestamp
from sqlalchemy import Column, BigInteger, VARCHAR, ForeignKey, Integer, TIMESTAMP


class RawLink(Base):
    __tablename__ = "raw_links"

    id = Column(BigInteger, primary_key=True)
    type = Column(VARCHAR(15), nullable=False)
    owner_id = Column(BigInteger, nullable=False)
    access_key = Column(VARCHAR)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())

    def __init__(self, id: int, type: str, owner_id: int, access_key: str, user_id: int, **kwargs) -> None:
        super(RawLink, self).__init__(**kwargs)
        self.id = id
        self.type = type
        self.owner_id = owner_id
        self.access_key = access_key
        self.user_id = user_id
        self.add_time = timestamp()

    @staticmethod
    def get(id: int, local_session=session):
        return local_session.query(RawLink).filter(RawLink.id == id).first()

    @staticmethod
    def get_all_with_type(type: str, local_session=session) -> list:
        return local_session.query(RawLink).filter(RawLink.type == type).all()

    def get_attachment_string(self) -> str:
        return f"{self.type}{self.owner_id}_{self.id}{ f'_{self.access_key}' if self.access_key else '' }"
