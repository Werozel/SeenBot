from sqlalchemy import Column, Integer, VARCHAR, Binary
from globals import Base

class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key = True)