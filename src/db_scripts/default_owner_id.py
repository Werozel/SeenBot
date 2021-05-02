from typing import List

from sqlalchemy.orm import Session

from globals import session_factory
from libs.RawLink import RawLink
from libs.User import User
from libs.Picture import Picture


if __name__ == "__main__":
    session: Session = session_factory()
    all_pics: List[Picture] = session.query(Picture).all()
    for pic in all_pics:
        pic.owner_id = pic.user_id
        session.add(pic)
    session.commit()
    session.close()
