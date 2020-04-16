from sqlalchemy import Column, Integer, VARCHAR, Binary

class Picture:
    __tablename__ = 'pictures'

    id = Column(Integer, primary_key = True)