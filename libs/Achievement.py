from typing import Optional

from sqlalchemy import Column, Integer, VARCHAR

from globals import Base, session


# Перевалил за N баянов
# Скинул кучу годноты
# Очень много дает рейтинга
# Много мэшапов
# Король видосов
# Рарная реакция
# Долго не скидывал мемы
# Самый долгий стрик по дням
# Классификация по жанрам мемов
# Много спрашивает стату у бота
#
class Achievement(Base):
    __tablename__ = 'achievements'

    type = Column(VARCHAR, primary_key=True)
    name = Column(VARCHAR, nullable=False)

    @staticmethod
    def get(type: str, local_session=session) -> Optional['Achievement']:
        if not type:
            return None
        return local_session.query(Achievement).filter(Achievement.type == type).first

    @staticmethod
    def get_all(local_session=session):
        return local_session.query(Achievement).all()

    def __eq__(self, other):
        return self.type == other.type
    
