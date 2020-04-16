from sqlalchemy import Column, Integer, VARCHAR, Binary, DECIMAL, ForeignKey

from globals import Base

class Picture(Base):
    __tablename__ = 'pictures'

    id = Column(DECIMAL, primary_key=True)
    link = Column(VARCHAR(50), unique=True, nullable=False)
    ups = Column(Integer, default=0)
    downs = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Picture {str(id)}: {str(self.ups)} ups, {str(self.downs)} downs"