from sqlalchemy import Column, Integer, VARCHAR, Binary, DECIMAL, ForeignKey

from globals import Base

class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(DECIMAL, primary_key=True)
    link = Column(VARCHAR(50), unique=True, nullable=False)
    up = Column(Integer, default=0)
    down = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)