from sqlalchemy import Column, Integer, VARCHAR, TIMESTAMP
from sqlalchemy.orm import relationship
from globals import Base, api, session, timestamp
from libs.Picture import Picture
from libs.Phrase import Phrase
from libs.PicMessage import PicMessage


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)
    ups = Column(Integer, default=0)
    downs = Column(Integer, default=0)
    all_pics = Column(Integer, default=0)
    add_time = Column(TIMESTAMP, default=timestamp())

    pic_rel = relationship("Picture", backref="user")
    phrase_rel = relationship("Phrase", backref="user")
    msg_rel = relationship("PicMessage", backref="user")

    def __init__(self, id: int, **kwargs):
        super(User, self).__init__(**kwargs)
        self.id = id
        user = User.get(id)
        if not user:
            user = api.users.get(user_ids=self.id)[0]
            self.first_name = user.get("first_name")
            self.last_name = user.get("last_name")
            self.ups = self.downs = self.all_pics = 0
            self.add_time = timestamp()
        else:
            self.first_name = user.first_name
            self.last_name = user.last_name
            self.ups = user.ups
            self.downs = user.downs
            self.all_pics = user.all_pics
            self.add_time = user.add_time

    @staticmethod
    def get(id: int, local_session=session):
        return local_session.query(User).filter(User.id == id).first()

    def get_pics(self, local_session=session):
        return local_session.query(Picture).filter(Picture.id == self.id).all()

    def __eq__(self, other) -> bool:
        return self.id == other.id

    def __repr__(self) -> str:
        return f"User { str(self.id) }: {self.first_name} {self.last_name} - {str(self.ups)} ups, " \
               f"{str(self.downs)} downs, {str(self.all_pics)} all"

    def show_stat(self) -> str:
        return f"{self.first_name}: {self.ups}↑ {self.downs}↓ всего: {self.all_pics}"

    # Returns latest pic sent by this user
    def __get_latest_pic(self):
        pass
