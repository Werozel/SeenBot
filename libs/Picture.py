from sqlalchemy import Column, Integer, VARCHAR, Binary, DECIMAL, ForeignKey, TIMESTAMP
from globals import Base, timestamp, session

class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(DECIMAL, primary_key=True)
    link = Column(VARCHAR(50), unique=True, nullable=False)
    ups = Column(Integer, default=0)
    downs = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    add_time = Column(TIMESTAMP, default=timestamp())

    def __init__ (self, link: str, user_id: int, **kwargs):
        super(Picture, self).__init__(**kwargs)
        self.link = link
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

    @staticmethod
    def was_sent(picture) -> bool:
        return False

    def __repr__(self):
        return f"Picture {str(id)}: {str(self.ups)} ups, {str(self.downs)} downs"