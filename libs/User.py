from sqlalchemy import Column, Integer, VARCHAR
from sqlalchemy.orm import relationship
from globals import Base
from Picture import Picture

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)
    ups = Column(Integer, default=0)
    downs = Column(Integer, default=0)
    all_pics = Column(Integer, default=0)

    pic_rel = relationship("Picture")


    def __repr__(self):
        return f"User { str(self.id) }: {self.first_name} {self.last_name} - {str(self.ups)} ups, {str(self.downs)} downs, {str(self.all_pics)} all"

    # Returns latest pic sent by this user
    def get_latest(self):
        pass